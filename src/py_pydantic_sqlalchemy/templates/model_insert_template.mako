def insert_${model.table_name}(session, data: dict[str, Any]) -> None:
    record = ${model.class_name}(
% for column in model.columns:
% if column.type_definition.nullable:
        ${column.name}=data.get("${column.name}"),
% else:
        ${column.name}=data["${column.name}"],
% endif
% endfor
    )
    session.add(record)

% if model.relationships:
% for relationship in [r for r in model.relationships if r.secondary]:
    ${relationship.related_table}_ids = data.get("${relationship.related_table}_ids", [])
    for related_record_id in ${relationship.related_table}_ids:
        related_record = ${relationship.class_name}(
            ${model.table_name}_id = data["id"],
            ${relationship.related_table}_id = related_record_id
        )
        session.add(related_record)

% endfor
% endif

