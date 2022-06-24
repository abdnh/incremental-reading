from typing import Callable

from aqt.qt import *
from aqt.utils import askUser, tr
import aqt.addcards
from aqt import gui_hooks

class AddCards(aqt.addcards.AddCards):
    def __init__(self, on_reject: Callable, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._on_reject = on_reject
        gui_hooks.add_cards_did_add_note.append(lambda _: self.close)

    def ifCanClose(self, onOk: Callable) -> None:
        def afterSave() -> None:
            ok = self.editor.fieldsAreBlank(self._last_added_note)
            want_close = False
            if not ok:
                want_close = askUser(
                    tr.adding_close_and_lose_current_input(), defaultno=True
                )
            if ok or want_close:
                onOk()
            if want_close:
                self._on_reject()

        self.editor.call_after_note_saved(afterSave)
