import os
import sqlite3
import json
import datetime
import flet as ft

DB_PATH = os.path.join(os.getenv("LOCALAPPDATA", "."), "alarms.db")

class AlarmRepository:
    def __init__(self, db_path: str = DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS Alarms (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Time TEXT NOT NULL,
            RepeatDays TEXT NOT NULL,
            Label TEXT,
            MelodyPath TEXT,
            Snooze INTEGER NOT NULL,
            IsActive INTEGER NOT NULL
            )"""
        )
        self.conn.commit()

    def list_alarms(self):
        cur = self.conn.execute(
            "SELECT Id, Time, RepeatDays, Label, MelodyPath, Snooze, IsActive FROM Alarms ORDER BY Time"
        )
        rows = cur.fetchall()
        return rows

    def add_alarm(self, time_str, repeat_days, label, melody, snooze, is_active):
        self.conn.execute(
            "INSERT INTO Alarms(Time, RepeatDays, Label, MelodyPath, Snooze, IsActive) VALUES (?, ?, ?, ?, ?, ?)",
            (time_str, json.dumps(repeat_days), label, melody, snooze, is_active),
        )
        self.conn.commit()

    def update_alarm(self, alarm_id, time_str, repeat_days, label, melody, snooze, is_active):
        self.conn.execute(
            "UPDATE Alarms SET Time=?, RepeatDays=?, Label=?, MelodyPath=?, Snooze=?, IsActive=? WHERE Id=?",
            (time_str, json.dumps(repeat_days), label, melody, snooze, is_active, alarm_id),
        )
        self.conn.commit()

    def delete_alarm(self, alarm_id):
        self.conn.execute("DELETE FROM Alarms WHERE Id=?", (alarm_id,))
        self.conn.commit()

    def toggle_alarm(self, alarm_id, active):
        self.conn.execute("UPDATE Alarms SET IsActive=? WHERE Id=?", (active, alarm_id))
        self.conn.commit()


class AlarmApp:
    """Simple alarm manager UI implemented with Flet."""

    def __init__(self, page: ft.Page, repo: AlarmRepository):
        self.page = page
        self.repo = repo
        self.dialog = None
        self.edit_id = None

        self.alarms_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Time")),
                ft.DataColumn(ft.Text("Label")),
                ft.DataColumn(ft.Text("Active")),
                ft.DataColumn(ft.Text("Actions")),
            ]
        )

        add_btn = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.open_add)
        self.container = ft.Column([self.alarms_table, add_btn])
        self.refresh()
        self.page.add(self.container)

    def refresh(self):
        rows = []
        for r in self.repo.list_alarms():
            alarm_id, time_str, _, label, _, _, active = r
            switch = ft.Switch(value=bool(active), on_change=self.make_toggle(alarm_id))
            edit_btn = ft.IconButton(icon=ft.icons.EDIT, on_click=self.make_edit(alarm_id))
            del_btn = ft.IconButton(icon=ft.icons.DELETE, on_click=self.make_delete(alarm_id))
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(time_str)),
                    ft.DataCell(ft.Text(label or "")),
                    ft.DataCell(switch),
                    ft.DataCell(ft.Row([edit_btn, del_btn])),
                ]
            )
            rows.append(row)
        self.alarms_table.rows = rows
        self.page.update()

    def make_toggle(self, alarm_id):
        def toggle(e):
            self.repo.toggle_alarm(alarm_id, 1 if e.control.value else 0)
        return toggle

    def make_edit(self, alarm_id):
        def edit(e):
            cur = [a for a in self.repo.list_alarms() if a[0] == alarm_id][0]
            time_str, repeat, label, melody, snooze, active = cur[1:7]
            self.edit_id = alarm_id
            self.open_dialog(time_str, json.loads(repeat), label, melody, snooze, active)
        return edit

    def make_delete(self, alarm_id):
        def delete(e):
            self.repo.delete_alarm(alarm_id)
            self.refresh()
        return delete

    def open_add(self, e):
        self.edit_id = None
        self.open_dialog("07:00", [], "", "", 0, 1)

    def open_dialog(self, time_str, repeat_days, label, melody, snooze, active):
        tp = ft.TimePicker(value=datetime.time.fromisoformat(time_str))
        label_field = ft.TextField(value=label, hint_text="Alarm")
        active_switch = ft.Switch(label="Active", value=bool(active))
        save_btn = ft.ElevatedButton("Save", on_click=lambda _: self.save_alarm(tp, label_field, active_switch))
        cancel_btn = ft.TextButton("Cancel", on_click=lambda _: self.close_dialog())
        self.dialog = ft.AlertDialog(
            modal=True,
            content=ft.Column([tp, label_field, active_switch], tight=True),
            actions=[cancel_btn, save_btn],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close_dialog(self):
        if self.dialog:
            self.dialog.open = False
            self.page.update()

    def save_alarm(self, time_picker, label_field, active_switch):
        time_value = time_picker.value.strftime("%H:%M")
        label = label_field.value
        active = 1 if active_switch.value else 0
        days = []
        melody = ""
        snooze = 0
        if self.edit_id is None:
            self.repo.add_alarm(time_value, days, label, melody, snooze, active)
        else:
            self.repo.update_alarm(self.edit_id, time_value, days, label, melody, snooze, active)
        self.close_dialog()
        self.refresh()


def main(page: ft.Page):
    page.title = "Alarms"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"
    repo = AlarmRepository()
    AlarmApp(page, repo)

if __name__ == "__main__":
    ft.app(target=main)
