import c4d
from c4d import utils

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def get_spline():
    """Gets the selected object as a Spline. Uses CSTO on parametrized splines. Returns None if invalid."""
    if op is None:
        c4d.gui.MessageDialog("Select an object.")
        return None

    if op.GetType() == c4d.Ospline:
        spline = op
    else:
        # If op is a parametrized spline (i.e. not c4d.Ospline) it has to be converted first.
        spline = apply_current_state_to_object(op)

        # If after CSTO the object is still not an Ospline the user did select a non-Spline object which is invalid.
        if spline.GetType() != c4d.Ospline:
            c4d.gui.MessageDialog("Select a Spline object.")
            return None

    return spline

def apply_current_state_to_object(obj):
    """Applies CSTO to obj in a new temporary document."""

    result = utils.SendModelingCommand(
        command=c4d.MCOMMAND_CURRENTSTATETOOBJECT,
        list=[obj],
        mode=c4d.MODELINGCOMMANDMODE_ALL,
        doc=c4d.documents.BaseDocument(),
        flags=c4d.MODELINGCOMMANDFLAGS_0)

    if not result:
        return None

    return result[0]

def get_desired_count():
    """Gets the desired amount of nulls to create by asking the user. Returns None if invalid."""
  
    count_str = c4d.gui.InputDialog("How many points would you like to create on the spline?", "10")

    try:
        return int(count_str)
    except ValueError:
        c4d.gui.MessageDialog("The entered value must be a whole number.")
        return None

def create_nulls_on_spline(spline, count):
    """Creates Nulls on a Spline with equal spacing based on the desired amount."""

    nulls = []

    for i in range(count):
        null = c4d.BaseObject(c4d.Onull)
        pos = spline.GetSplinePoint(1 / count * i)
        null.SetAbsPos(pos)
        null.SetName(f"Null_{i}")

        nulls.append(null)

    return nulls

def add_nulls_to_object(nulls, obj):
    """Adds nulls as children to obj."""
    doc.StartUndo()

    for i, null in enumerate(nulls):
        null.InsertUnderLast(obj)

        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, null)
        doc.SetActiveObject(null, c4d.SELECTION_NEW if i == 0 else c4d.SELECTION_ADD)

    doc.EndUndo()
    c4d.EventAdd()

def main() -> None:
    spline = get_spline();

    if not spline:
        return

    count = get_desired_count();

    if not count:
        return

    nulls = create_nulls_on_spline(spline, count)

    add_nulls_to_object(nulls, op)

if __name__ == '__main__':
    main()
