from prefixdate import parse_parts

from opensanctions import helpers as h
from opensanctions.util import remove_namespace


def parse_address(context, el):
    country = el.get("countryDescription")
    if country == "UNKNOWN":
        country = None
    # context.log.info("Addrr", el=el)
    return h.make_address(
        context,
        street=el.get("street"),
        po_box=el.get("poBox"),
        city=el.get("city"),
        place=el.get("place"),
        postal_code=el.get("zipCode"),
        region=el.get("region"),
        country=country,
        country_code=el.get("countryIso2Code"),
    )


def parse_entry(context, entry):
    subject_type = entry.find("./subjectType")
    schema = context.lookup_value("subject_type", subject_type.get("code"))
    if schema is None:
        context.log.warning("Unknown subject type", type=subject_type)
        return

    entity = context.make(schema)
    entity.id = context.make_slug(entry.get("euReferenceNumber"))
    entity.add("notes", entry.findtext("./remark"))
    entity.add("topics", "sanction")

    sanction = h.make_sanction(context, entity)
    regulation = entry.find("./regulation")
    source_url = regulation.findtext("./publicationUrl", "")
    sanction.set("sourceUrl", source_url)
    sanction.add("program", regulation.get("programme"))
    sanction.add("reason", regulation.get("numberTitle"))
    sanction.add("startDate", regulation.get("entryIntoForceDate"))
    sanction.add("listingDate", regulation.get("publicationDate"))

    for name in entry.findall("./nameAlias"):
        if entry.get("strong") == "false":
            entity.add("weakAlias", name.get("wholeName"))
        else:
            entity.add("name", name.get("wholeName"))
        entity.add("title", name.get("title"), quiet=True)
        entity.add("firstName", name.get("firstName"), quiet=True)
        entity.add("middleName", name.get("middleName"), quiet=True)
        entity.add("lastName", name.get("lastName"), quiet=True)
        entity.add("position", name.get("function"), quiet=True)
        gender = h.clean_gender(name.get("gender"))
        entity.add("gender", gender, quiet=True)

    for node in entry.findall("./identification"):
        type = node.get("identificationTypeCode")
        schema = "Passport" if type == "passport" else "Identification"
        passport = context.make(schema)
        passport.id = context.make_id("ID", entity.id, node.get("logicalId"))
        passport.add("holder", entity)
        passport.add("authority", node.get("issuedBy"))
        passport.add("type", node.get("identificationTypeDescription"))
        passport.add("number", node.get("number"))
        passport.add("number", node.get("latinNumber"))
        passport.add("startDate", node.get("issueDate"))
        passport.add("startDate", node.get("issueDate"))
        passport.add("country", node.get("countryIso2Code"))
        passport.add("country", node.get("countryDescription"))
        for remark in node.findall("./remark"):
            passport.add("summary", remark.text)
        context.emit(passport)

    for node in entry.findall("./address"):
        address = parse_address(context, node)
        h.apply_address(context, entity, address)

        for child in node.getchildren():
            if child.tag in ("regulationSummary"):
                continue
            elif child.tag == "remark":
                entity.add("notes", child.text)
            elif child.tag == "contactInfo":
                prop = context.lookup_value("contact_info", child.get("key"))
                if prop is None:
                    context.log.warning("Unknown contact info", node=child)
                else:
                    entity.add(prop, child.get("value"))
            else:
                context.log.warning("Unknown address component", node=child)

    for birth in entry.findall("./birthdate"):
        partialBirth = parse_parts(
            birth.get("year"), birth.get("month"), birth.get("day")
        )
        entity.add("birthDate", birth.get("birthdate"))
        entity.add("birthDate", partialBirth)
        address = parse_address(context, birth)
        if address is not None:
            entity.add("birthPlace", address.get("full"))
            entity.add("country", address.get("country"))

    for node in entry.findall("./citizenship"):
        entity.add("nationality", node.get("countryIso2Code"), quiet=True)
        entity.add("nationality", node.get("countryDescription"), quiet=True)

    context.emit(entity, target=True, unique=True)
    context.emit(sanction)


def crawl(context):
    path = context.fetch_resource("source.xml", context.dataset.data.url)
    context.export_resource(path, "text/xml", title=context.SOURCE_TITLE)
    doc = context.parse_resource_xml(path)
    doc = remove_namespace(doc)
    for entry in doc.findall(".//sanctionEntity"):
        parse_entry(context, entry)
