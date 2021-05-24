import goost


def can_build(env, platform):
    return True


def configure(env):
    from SCons.Script import Variables, BoolVariable, Help, Exit

    # Check dependencies.
    dependencies_satisfied = True
    for c in goost.classes_enabled:
        resolved = goost.resolve_dependency(goost.classes[c])
        for cr in resolved:
            if cr not in goost.classes_enabled:
                dependencies_satisfied = False
                print("Goost: Cannot disable `%s` class, because `%s` class depends on it." % (cr, c))

    if not dependencies_satisfied:
        Exit(255)

    opts = Variables()
    for name in goost.get_components():
        opts.Add(BoolVariable("goost_%s_enabled" % (name), "Build %s component." % (name), True))

    opts.Add("goost_scale_factor", "The precision used for converting between integer and float coordinates.", "1e5")

    opts.Update(env)

    # Get a list of components which got disabled.
    disabled = []
    for name in goost.get_components():
        if not env["goost_%s_enabled" % (name)]:
            disabled.append(name)

    # Implicitly disable child components.
    for name in disabled:
        children = goost.get_child_components(name)
        for child_name in children:
            print("Goost: Disabling `%s` component (part of `%s`)." % (child_name, name))
            env["goost_%s_enabled" % (child_name)] = False

    def help_format(env, opt, help, default, actual, aliases):
        if opt == "goost_scale_factor":
            fmt = "\n%s: %s.\n    default: %s (based on CMP_EPSILON)\n    actual: %s\n"
        else:
            fmt = "\n%s: %s.\n    default: %s\n    actual: %s\n"
        return fmt % (opt, help, default, actual)

    opts.FormatVariableHelpText = help_format
    Help(opts.GenerateHelpText(env))


def get_doc_classes():
    return goost.classes.keys()


def get_doc_path():
    return "doc"


def get_icons_path():
    return "editor/icons"    


def get_modules_path():
    return "modules"
