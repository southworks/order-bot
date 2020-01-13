from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus

from data_models import Add, Remove, Confirm


class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog,
        turn_context: TurnContext,
        accessor: StatePropertyAccessor,
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)

    @staticmethod
    def recognize_intention(text):
        if "add" in text:
            return Add()
        elif "remove" in text:
            return Remove()
        elif "confirm" in text:
            return Confirm()
