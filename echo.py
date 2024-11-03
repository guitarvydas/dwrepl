import py0dws as zd


def install (reg):
    zd.register_component (reg, zd.Template ("Echo", None, instantiator))

def handler (eh, msg):
    zd.send_string (eh, "", msg.datum.srepr (), msg)
def instantiator (reg, owner, name, template_data):
    name_with_id = zd.gensymbol ("Echo")
    return zd.make_leaf (name_with_id, owner, None, handler)
