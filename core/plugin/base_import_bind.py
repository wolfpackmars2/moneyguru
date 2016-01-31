# Copyright 2016 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from core.plugin import ImportBindPlugin, EntryMatch

class ReferenceBind(ImportBindPlugin):
    NAME = "Reference Import Bind"
    AUTHOR = "Nelson Brown"

    def match_entries(self,
                      target_account,
                      document,
                      import_document,
                      existing_entries,
                      imported_entries):
        matches = []
        import_reference2entry = {}
        will_import = True
        for import_entry in (e for e in imported_entries if e.reference):
            import_reference2entry[import_entry.reference] = import_entry

        for existing_entry in existing_entries:
            if existing_entry.reference in import_reference2entry:
                import_entry = import_reference2entry[existing_entry.reference]
                if existing_entry.reconciled:
                    will_import = False

                del import_reference2entry[existing_entry.reference]
            else:
                import_entry = None

            if import_entry is not None:
                matches.append(EntryMatch(existing_entry, import_entry, will_import, 0.99))
            elif not will_import:
                matches.append(EntryMatch(existing_entry, import_entry, will_import, 0.99))

        return matches

