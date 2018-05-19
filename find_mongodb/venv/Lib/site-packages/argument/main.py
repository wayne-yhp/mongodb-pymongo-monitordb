import sys
class Mux(object):
    def __init__(self, d = None):
        self.commands = {}
        for k,v in d.items():
            self.commands[k] = v

    
    def match(self, name, a):
        self.commands[name] = a

    def parse(self, args=None):
        if not args:
            args = sys.argv
            
        if len(args) == 1:
            return None, [IndexError("No command supplied" )]
        
        cmd = args[1]
        resargs = args[2:]
        if cmd in self.commands:
            return self.commands[cmd].parse(args[2:])
        return None, [IndexError("Command not found: %s" % cmd)]
        
    def help_usage(self):
        lines = []
        for n in sorted(self.commands):
            p = "%s %s" % (sys.argv[0], n)
            lines.append(self.commands[n].help_usage(p))
        return "\n".join(lines)
    
    def __str__(self):
        return self.help_usage().rstrip()
    def __unicode__(self):
        return unicode(self).encode("utf-8")


class Arguments(object):

    def __init__(self):
        self.required = []
        self.maybes = []

        self.data = {}
        self.text = {
            'switch': {},
            'option': {},
            'required': {},
            'maybe': {},
        }
        self.names = {
            'switches': [],
            'options': [],
        }
        self.abbr = {}
        self.processors = {}
        self.validators = {}

    def _set_default_value(self, name, value):
        if name in self.data:
            raise ValueError("%s is already used" % name)
        self.data[name] = value

    def _set_abbr(self, name, abbr):
        if abbr in self.abbr:
            raise ValueError("%s is already used" % abbr)
        self.abbr[abbr] = name
    
    def switch(self, name, help=u"N/A", abbr=""):
        self._set_default_value(name, False)

        self.names['switches'].append(name)
        self.text['switch'][name] = help
        if abbr:
            self._set_abbr(name, abbr)

    def option(self, name, value, help=u"N/A", abbr=None):
        self._set_default_value(name, value)

        self.text['option'][name] = help
        if abbr:
            self.abbr[abbr] = name

    def always(self, name, help="N/A"):
        self.required.append(name)
        self._set_default_value(name, None)
        self.text['required'][name] = help

    def maybe(self, name, help="N/A"):
        self.maybes.append(name)
        self._set_default_value(name, None)
        self.text['maybe'][name] = help
    
    def process(self, name, fun):
        if name not in self.processors:
            self.processors[name] = []
        self.processors[name].append(fun)

    def validate(self, name, fun, exp="Validation failed"):
        if name not in self.validators:
            self.validators[name] = []
        self.validators[name].append((fun, exp))

    def elongate(self, abbr):
        return self.abbr[abbr]

    def is_value(self, name):
        return name in self.data

    def is_switch(self, name):
        return name in self.names['switches']

    def is_abbr(self, name):
        return name in self.abbr

    def _parse_args(self, args):
        requested = {}
        ordinal = []
        for a in args:
            # require arguments
            if a[0] != "-":
                ordinal.append(a)
                continue
            #there is assigment, options
            if "=" in a:
                raw, value = a.split("=")
                if len(raw) > 3 and raw[0:2] == "--":
                    name = raw.strip("-")
                    requested[name] = value
                else:
                    requested[raw.strip("-")] = value
                continue
            # swtiches
            if len(a) > 2 and a[0:2] == "--":
                name = a[2:]
                requested[name] = True
                continue

            if a[0] == "-":
                for x in a[1:]:
                    requested[x] = True

        return requested, ordinal

    def parse(self, args=None):
        if args is None:
            args = sys.argv[1:]
        
        requested, ordinal = self._parse_args(args)

        results = {}
        errors = []
        # set defaults
        for k in self.data:
            results[k] = self.data[k]
        # set ordinal
        for e, value in enumerate(ordinal):
            o = e - len(self.required)
            if e < len(self.required):
                name = self.required[e]
                results[name] = value
            elif o < len(self.maybes):
                name = self.maybes[o]
                results[name] = value
            else:
                errors.append(IndexError("Unnamed arguments found: [%s]" % value))
        
        # set optional
        for name, value in requested.items():
            if self.is_abbr(name):
                name = self.elongate(name)
            if self.is_switch(name):
                results[name] = True
            elif self.is_value(name):
                if value == True:
                    errors.append(
                        TypeError(
                        "Value argument used without value: [%s]" %
                        name)
                    )
                    continue
                results[name] = value
            else:
                errors.append(ValueError("Unkown argument: [%s]" % name))

        # processor
        for name, processors in self.processors.items():
            for p in processors:
                if results[name]:
                    try:
                        results[name] = p(results[name])
                    except Exception as e:
                        errors.append(e)
        
        # validators    
        for name, funs in self.validators.items():
            for f, exp in funs:
                if not f(results[name]):
                    errors.append(AssertionError("[%s] %s" % (name, exp)))

        # check mandatory
        if len(ordinal) < len(self.required):
            missing = self.required[len(ordinal):]
            errors.append(ValueError(
                "Number of require arguments mismatch, missing: %s" %
                (",".join(missing)))
                )
        
        return results, errors

    def help_usage(self, prefix=None):
        if not prefix:
            prefix = sys.argv[0]

        usage_options = ""
        options_count = len([x for x in self.names.items()])
        if options_count > 0:
            usage_options = " [OPTIONS] "

        mandatory = " ".join(self.required).upper()

        length_name = sorted([len(x) for x in self.names.keys()])[-1]
        length_values = sorted([len(str(x)) for x in self.data.values()])[-1]
        len_just = length_name + length_values + 5

        abbr_reverse = dict([(v, k) for k, v in self.abbr.items()])
        r = ""
        r += "Usage: " + prefix + usage_options + mandatory
        r += "\n\n"
        if len(self.required) > 0:
            r += "Required arguments:\n"
            for k, v in self.text['required'].items():
                r += " " + k.ljust(len_just).upper() + " " * 6 + v
                r += "\n"
            r += "\n"

        if len(self.maybes) > 0:
            r += "Optional arguments:\n"
            for k, v in self.text['maybe'].items():
                r += " " + k.ljust(len_just).upper() + " " * 6 + v
                r += "\n"
            r += "\n"

        if len(self.text["option"]) > 0:
            r += "Options:\n"
            for k, v in self.text["option"].items():
                a = ""
                if k in abbr_reverse:
                    a = "-" + abbr_reverse[k]
                a = " " + a.rjust(2)
                nv = "--%s=%s" % (k, self.data[k])
                r += a + "  " + nv.ljust(len_just) + " " * 2 + v
                r += "\n"

        if len(self.text["switch"]) > 0:
            r += "\nSwitches:\n"
            for k, v in self.text["switch"].items():
                a = ""
                if k in abbr_reverse:
                    a = "-" + abbr_reverse[k]
                a = " " + a.rjust(2)
                nv = "--%s" % (k)
                r += a + "  " + nv.ljust(len_just) + " " * 2 + v
                r += "\n"

        return r
    def __str__(self):
        return self.help_usage().rstrip()
    def __unicode__(self):
        return unicode(self).encode("utf-8")
