import sublime
import sublime_plugin
from SublimeLinter.lint import persist


class LinterNameInputHandler(sublime_plugin.ListInputHandler):
    def list_items(self):
        return (
            ['SublimeLinter'] +
            sorted(name for name in persist.linter_classes.keys())
        )


class sl_addon_show_readmes(sublime_plugin.WindowCommand):
    def run(self, linter_name):
        if linter_name == 'SublimeLinter':
            package_name = 'SublimeLinter'
        else:
            try:
                klass = persist.linter_classes[linter_name]
            except KeyError:
                self.window.status_message(
                    "'{}' is not registered.".format(linter_name))
                return
            else:
                package_name = klass.__module__.split('.')[0]

        relative_path_to_readme = "{}/README.md".format(package_name)
        try:
            sublime.load_resource('Packages/' + relative_path_to_readme)
        except OSError:
            self.window.status_message(
                "No README.md found for '{}'".format(linter_name))
        else:
            path_to_readme = "${packages}/" + relative_path_to_readme
            self.window.run_command('open_file', {'file': path_to_readme})

    def input(self, _args):
        return LinterNameInputHandler()
