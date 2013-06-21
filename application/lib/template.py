from tornado.template import Template

def render(template_file, data={}):

    t = Template(open("public/views/{0}".format(template_file), "r").read())
    return t.generate(**data)