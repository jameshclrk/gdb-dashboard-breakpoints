class Breakpoints(Dashboard.Module):
    """Show the current breakpoints and their values."""

    avail_breaks = {
            gdb.BP_BREAKPOINT: "breakpoint",
            gdb.BP_WATCHPOINT: "(W)  ",
            gdb.BP_HARDWARE_WATCHPOINT: "(W)  ",
            gdb.BP_READ_WATCHPOINT: "(R)  ",
            gdb.BP_ACCESS_WATCHPOINT: "(R/W)"
            }

    def __init__(self):
        self.table = {}

    def label(self):
        return 'Breakpoints'

    def lines(self, term_width, style_changed):
        breakpoints = gdb.breakpoints()
        output = []
        if (len(breakpoints) == 0):
            return output
        for bp in breakpoints:
            number = ansi(bp.number, R.style_selected_1)
            hits = ansi(bp.hit_count, R.style_selected_2) + " hit"
            temp = ansi("[temp]", R.style_high) if bp.temporary else ""
            if (bp.hit_count != 1):
                hits += "s"
            bp_type = Breakpoints.avail_breaks.get(bp.type, "unknown")
            if (bp.type == gdb.BP_BREAKPOINT):
                message = bp.location
            else:
                try:
                    value = to_string(gdb.parse_and_eval(bp.expression))
                except gdb.error as e:
                    value = ansi(e, R.style_error)
                message = bp_type + " " + bp.expression + " = " + value
            if (bp.condition):
                message += " if " + bp.condition
            output.append('[{}] {} [{}] {}'.format(number, message, hits, temp))
        return output

