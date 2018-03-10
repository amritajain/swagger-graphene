import graphene


class SwaggerWrapper:

    datatype_mapper = {
        'integer': graphene.Int,
        'string': graphene.String,
        'number': graphene.Float,
        'boolean': graphene.Boolean
    }
    swagger_definitions = {}

    def __init__(self, swagger_definitions, api_data):
        self.__class__.swagger_definitions = swagger_definitions
        self.__class__.api_data = api_data


    def swagger_to_graphene(self, model):

        fields = self.__class__.generate_fields(self, self.__class__.swagger_definitions[model]['properties'])
        return fields

    def generate_fields(self, swagger_datatype):

        fields = {}
        for field in swagger_datatype:

            if "$ref" in swagger_datatype[field]:
                graphene_object = self.__class__.handle_nested_object(self, swagger_datatype[field])
                try:
                    resolver_object = self.__class__.api_data[field]
                    fields[field] = graphene.Field(graphene_object,
                                                   resolver=lambda obj, args, context, info: graphene_object(
                                                       **resolver_object))
                except KeyError:
                    fields[field] = graphene.Field(graphene_object,
                                                   resolver=lambda obj, args, context, info: obj[field])



            elif "array" in swagger_datatype[field]['type']:
                fields[field] = self.__class__.handle_array(self, swagger_datatype[field])

            else:
                fields[field] = self.__class__.datatype_mapper[swagger_datatype[field]['type']]()

        return fields

    def handle_array(self, swagger_datatype):

        if "type" in swagger_datatype['items']:
            list_type = swagger_datatype['items']['type']
            result = graphene.List(self.datatype_mapper[list_type])
        else :
            graphene_subtype = self.__class__.handle_list_object(self, swagger_datatype['items'])
            result = graphene.List(graphene_subtype)

        return result

    def handle_nested_object(self, swagger_datatype):
        parent_object_type = swagger_datatype["$ref"].split("/").pop()

        parent_object = self.__class__.generate_fields(self, self.__class__.swagger_definitions[parent_object_type]['properties'])

        field_object = type(parent_object_type, (graphene.ObjectType,), parent_object)

        return field_object

    def handle_list_object(self, swagger_datatype):
        parent_object_type = swagger_datatype["$ref"].split("/").pop()

        parent_object = self.__class__.generate_fields(self, self.__class__.swagger_definitions[parent_object_type]['properties'])
        list_object = {}

        for item in parent_object:
            temp_obj = getattr(graphene, parent_object[item]._meta.name)
            list_object[item] = self.generate_resolver(temp_obj, item)

        field_object = type(parent_object_type, (graphene.ObjectType,), list_object, )
        return field_object

    def generate_resolver(self, temp_obj, item):
        return temp_obj(resolver=lambda obj, args, context, info: obj[item])

# @todo: enums