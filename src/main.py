"""
AquaGuard – Community Water Quality & Usage Monitor
====================================================
HACK-AI-THON 2026 | National Level Project
Theme: Python Fundamentals + OOP + SDG 6 & SDG 12

Beautiful modern GUI built with PySide6.
"""

from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from typing import List

from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QLineEdit, QComboBox, QDateEdit,
    QDoubleSpinBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QStackedWidget, QMessageBox, QTextEdit, QGraphicsDropShadowEffect
)
from PySide6.QtCharts import (
    QChart, QChartView, QPieSeries, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis
)


# =============================================================================
# 1. DOMAIN CLASSES (OOP – required by problem statement)
# =============================================================================

class Location:
    def __init__(self, name: str, address: str, location_type: str = "Household"):
        self.name = name
        self.address = address
        self.location_type = location_type

    def __str__(self) -> str:
        return f"{self.name} ({self.location_type})"


class User:
    def __init__(self, user_id: str, name: str, role: str = "Resident"):
        self.user_id = user_id
        self.name = name
        self.role = role

    def __str__(self) -> str:
        return self.name


class WaterReading:
    PH_MIN = 6.5
    PH_MAX = 8.5
    TURBIDITY_LIMIT = 5.0
    CONSUMPTION_LIMIT = 450.0

    def __init__(self, reading_date: date, location: Location, recorded_by: User,
                 consumption: float, ph: float, turbidity: float):
        self.reading_date = reading_date
        self.location = location
        self.recorded_by = recorded_by
        self.consumption = float(consumption)
        self.ph = float(ph)
        self.turbidity = float(turbidity)

    def is_abnormal(self) -> bool:
        return (self.ph < self.PH_MIN or self.ph > self.PH_MAX or
                self.turbidity > self.TURBIDITY_LIMIT or
                self.consumption > self.CONSUMPTION_LIMIT)

    def get_alerts(self) -> List[str]:
        alerts = []
        if self.ph < self.PH_MIN:
            alerts.append(f"Low pH ({self.ph:.1f})")
        elif self.ph > self.PH_MAX:
            alerts.append(f"High pH ({self.ph:.1f})")
        if self.turbidity > self.TURBIDITY_LIMIT:
            alerts.append(f"High turbidity ({self.turbidity:.1f} NTU)")
        if self.consumption > self.CONSUMPTION_LIMIT:
            alerts.append(f"High consumption ({self.consumption:.0f} L)")
        return alerts

    def quality_status(self) -> str:
        return "ABNORMAL" if self.is_abnormal() else "NORMAL"


class MonitoringReport:
    def __init__(self, report_id: str, generated_by: User, location: Location):
        self.report_id = report_id
        self.generated_by = generated_by
        self.location = location
        self.readings: List[WaterReading] = []
        self.generated_at = datetime.now()

    def add_reading(self, reading: WaterReading) -> None:
        self.readings.append(reading)

    def average_consumption(self) -> float:
        if not self.readings:
            return 0.0
        return sum(r.consumption for r in self.readings) / len(self.readings)

    def consumption_trend(self) -> str:
        if len(self.readings) < 2:
            return "Not enough data"
        sorted_r = sorted(self.readings, key=lambda x: x.reading_date)
        first, last = sorted_r[0].consumption, sorted_r[-1].consumption
        if last > first * 1.15:
            return "Increasing ⬆"
        if last < first * 0.85:
            return "Decreasing ⬇"
        return "Stable →"

    def status(self) -> str:
        return "ATTENTION NEEDED ⚠" if any(r.is_abnormal() for r in self.readings) else "NORMAL ✓"

    def get_all_alerts(self) -> List[str]:
        alerts = []
        for r in self.readings:
            for a in r.get_alerts():
                alerts.append(f"{r.reading_date}: {a}")
        return alerts

    def recommendations(self) -> List[str]:
        recs = []
        if self.average_consumption() > 400:
            recs.append("Reduce daily water use. Check for leaks or dripping taps.")
        if "Increasing" in self.consumption_trend():
            recs.append("Usage is rising. Avoid unnecessary water use and fix leaks promptly.")
        alerts = self.get_all_alerts()
        if any("turbidity" in a.lower() for a in alerts):
            recs.append("High turbidity detected → Use filtration or boil water before drinking.")
        if any("pH" in a for a in alerts):
            recs.append("pH out of safe range → Get water tested by a certified lab.")
        if not recs:
            recs.append("Everything looks normal. Keep conserving water!")
        return recs

    def generate_text(self) -> str:
        lines = [
            "=" * 62,
            "               AQUAGUARD MONITORING REPORT",
            "=" * 62,
            f"Report ID       : {self.report_id}",
            f"Location        : {self.location}",
            f"Generated by    : {self.generated_by}",
            f"Generated on    : {self.generated_at.strftime('%d %b %Y, %I:%M %p')}",
            "-" * 62,
            f"Status          : {self.status()}",
            f"Total Readings  : {len(self.readings)}",
            f"Avg Consumption : {self.average_consumption():.1f} L/day",
            f"Trend           : {self.consumption_trend()}",
            "-" * 62,
            "",
            "ALERTS:",
        ]
        alerts = self.get_all_alerts()
        if alerts:
            lines.extend(f"  • {a}" for a in alerts)
        else:
            lines.append("  • No abnormal readings")
        lines.append("")
        lines.append("RECOMMENDATIONS:")
        lines.extend(f"  → {r}" for r in self.recommendations())
        lines.append("")
        lines.append("=" * 62)
        return "\n".join(lines)


# =============================================================================
# 2. UI HELPERS
# =============================================================================

def apply_shadow(widget: QWidget, blur: int = 18, y_offset: int = 4, alpha: int = 30) -> None:
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur)
    shadow.setXOffset(0)
    shadow.setYOffset(y_offset)
    shadow.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(shadow)


COLORS = {
    "bg": "#F0F7FA",
    "sidebar": "#FFFFFF",
    "card": "#FFFFFF",
    "primary": "#0EA5E9",
    "primary_dark": "#0284C7",
    "accent": "#14B8A6",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "text": "#0F172A",
    "muted": "#64748B",
    "border": "#E2E8F0",
}


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str = "", accent: str = COLORS["primary"]):
        super().__init__()
        self.setObjectName("metricCard")
        self.setFixedHeight(110)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(4)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet(f"color: {COLORS['muted']}; font-size: 12px; font-weight: 600;")
        layout.addWidget(lbl_title)

        self.lbl_value = QLabel(value)
        self.lbl_value.setStyleSheet(f"color: {COLORS['text']}; font-size: 26px; font-weight: 700;")
        layout.addWidget(self.lbl_value)

        self.lbl_sub = QLabel(subtitle)
        self.lbl_sub.setStyleSheet(f"color: {accent}; font-size: 11px; font-weight: 500;")
        layout.addWidget(self.lbl_sub)

        self.setStyleSheet(f"""
            #metricCard {{
                background: {COLORS['card']};
                border-radius: 14px;
                border: 1px solid {COLORS['border']};
            }}
        """)
        apply_shadow(self, blur=16, y_offset=3, alpha=25)

    def update_value(self, value: str, subtitle: str = "") -> None:
        self.lbl_value.setText(value)
        if subtitle:
            self.lbl_sub.setText(subtitle)


class SidebarButton(QPushButton):
    def __init__(self, text: str, active: bool = False):
        super().__init__(text)
        self.setCheckable(True)
        self.setChecked(active)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(44)
        self.setStyleSheet(f"""
            QPushButton {{
                text-align: left;
                padding-left: 18px;
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 600;
                color: {COLORS['muted']};
                background: transparent;
            }}
            QPushButton:hover {{
                background: #F1F5F9;
                color: {COLORS['text']};
            }}
            QPushButton:checked {{
                background: #E0F2FE;
                color: {COLORS['primary_dark']};
            }}
        """)


# =============================================================================
# 3. MAIN WINDOW
# =============================================================================

class AquaGuardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AquaGuard • Water Quality & Usage Monitor")
        self.resize(1280, 780)
        self.setMinimumSize(1100, 700)

        self.readings: List[WaterReading] = []
        self._load_sample_data()
        self._build_ui()
        self._refresh_all()

    def _load_sample_data(self) -> None:
        loc1 = Location("Green Villa", "Sector 12, Noida", "Household")
        loc2 = Location("Sunrise Apt", "Block B, Delhi", "Household")
        loc3 = Location("City Public School", "Sector 15, Noida", "School")

        user1 = User("U101", "Priya Sharma")
        user2 = User("U102", "Rahul Verma")
        user3 = User("U103", "Ananya Gupta")

        today = date.today()
        self.readings = [
            WaterReading(today - timedelta(days=4), loc1, user1, 310, 7.2, 2.1),
            WaterReading(today - timedelta(days=3), loc1, user1, 325, 7.0, 2.4),
            WaterReading(today - timedelta(days=2), loc1, user1, 480, 6.3, 3.0),
            WaterReading(today - timedelta(days=1), loc1, user1, 510, 7.1, 6.8),
            WaterReading(today - timedelta(days=3), loc2, user2, 290, 7.4, 1.8),
            WaterReading(today - timedelta(days=2), loc2, user2, 305, 7.3, 2.0),
            WaterReading(today - timedelta(days=1), loc2, user2, 298, 7.5, 1.9),
            WaterReading(today - timedelta(days=2), loc3, user3, 820, 7.1, 2.5),
            WaterReading(today - timedelta(days=1), loc3, user3, 790, 6.9, 2.2),
            WaterReading(today,                     loc3, user3, 850, 7.0, 4.1),
        ]

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(230)
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet(f"""
            #sidebar {{
                background: {COLORS['sidebar']};
                border-right: 1px solid {COLORS['border']};
            }}
        """)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(16, 20, 16, 20)
        side_layout.setSpacing(6)

        brand = QLabel("💧  AquaGuard")
        brand.setStyleSheet(f"font-size: 20px; font-weight: 800; color: {COLORS['primary_dark']};")
        side_layout.addWidget(brand)

        tagline = QLabel("Clean Water • Responsible Use")
        tagline.setStyleSheet(f"color: {COLORS['muted']}; font-size: 11px; margin-bottom: 12px;")
        side_layout.addWidget(tagline)
        side_layout.addSpacing(12)

        self.btn_dash = SidebarButton("Dashboard", active=True)
        self.btn_add = SidebarButton("Add Reading")
        self.btn_list = SidebarButton("All Readings")
        self.btn_report = SidebarButton("Generate Report")
        self.btn_about = SidebarButton("About / SDG")

        for b in (self.btn_dash, self.btn_add, self.btn_list, self.btn_report, self.btn_about):
            side_layout.addWidget(b)

        side_layout.addStretch()

        sdg_box = QFrame()
        sdg_box.setStyleSheet("background: #ECFDF5; border-radius: 12px;")
        sdg_layout = QVBoxLayout(sdg_box)
        sdg_layout.setContentsMargins(12, 10, 12, 10)
        sdg_lbl = QLabel("SDG 6 & SDG 12")
        sdg_lbl.setStyleSheet("font-weight: 700; color: #059669; font-size: 12px;")
        sdg_layout.addWidget(sdg_lbl)
        sdg_sub = QLabel("Clean Water &\nResponsible Consumption")
        sdg_sub.setStyleSheet("color: #047857; font-size: 11px;")
        sdg_layout.addWidget(sdg_sub)
        side_layout.addWidget(sdg_box)

        main_layout.addWidget(sidebar)

        # Content
        content = QWidget()
        content.setStyleSheet(f"background: {COLORS['bg']};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 18, 24, 18)
        content_layout.setSpacing(16)

        header = QHBoxLayout()
        self.page_title = QLabel("Dashboard")
        self.page_title.setStyleSheet(f"font-size: 22px; font-weight: 700; color: {COLORS['text']};")
        header.addWidget(self.page_title)
        header.addStretch()
        date_lbl = QLabel(datetime.now().strftime("%A, %d %B %Y"))
        date_lbl.setStyleSheet(f"color: {COLORS['muted']}; font-size: 13px;")
        header.addWidget(date_lbl)
        content_layout.addLayout(header)

        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack)

        self.page_dashboard = self._create_dashboard_page()
        self.page_add = self._create_add_page()
        self.page_list = self._create_list_page()
        self.page_report = self._create_report_page()
        self.page_about = self._create_about_page()

        self.stack.addWidget(self.page_dashboard)
        self.stack.addWidget(self.page_add)
        self.stack.addWidget(self.page_list)
        self.stack.addWidget(self.page_report)
        self.stack.addWidget(self.page_about)

        main_layout.addWidget(content)

        self.btn_dash.clicked.connect(lambda: self._switch_page(0, "Dashboard"))
        self.btn_add.clicked.connect(lambda: self._switch_page(1, "Add Reading"))
        self.btn_list.clicked.connect(lambda: self._switch_page(2, "All Readings"))
        self.btn_report.clicked.connect(lambda: self._switch_page(3, "Generate Report"))
        self.btn_about.clicked.connect(lambda: self._switch_page(4, "About / SDG"))

        self.setStyleSheet(f"""
            QMainWindow, QWidget {{ font-family: 'Segoe UI', 'Arial', sans-serif; }}
            QLineEdit, QDoubleSpinBox, QDateEdit, QComboBox {{
                padding: 8px 12px;
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                background: white;
                font-size: 13px;
                min-height: 18px;
            }}
            QLineEdit:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
                border: 1.5px solid {COLORS['primary']};
            }}
            QPushButton#primaryBtn {{
                background: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }}
            QPushButton#primaryBtn:hover {{ background: {COLORS['primary_dark']}; }}
            QPushButton#secondaryBtn {{
                background: #F1F5F9;
                color: {COLORS['text']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: 600;
            }}
            QTableWidget {{
                background: white;
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                gridline-color: {COLORS['border']};
                font-size: 12px;
            }}
            QHeaderView::section {{
                background: #F8FAFC;
                padding: 10px;
                border: none;
                border-bottom: 1px solid {COLORS['border']};
                font-weight: 600;
                color: {COLORS['muted']};
            }}
        """)

    def _switch_page(self, index: int, title: str) -> None:
        self.stack.setCurrentIndex(index)
        self.page_title.setText(title)
        for i, btn in enumerate([self.btn_dash, self.btn_add, self.btn_list, self.btn_report, self.btn_about]):
            btn.setChecked(i == index)
        if index == 0:
            self._refresh_dashboard()
        elif index == 2:
            self._refresh_table()
        elif index == 3:
            self._populate_report_locations()

    # -------------------- DASHBOARD --------------------
    def _create_dashboard_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        cards = QHBoxLayout()
        cards.setSpacing(14)
        self.card_total = MetricCard("Total Readings", "0", "All locations")
        self.card_avg = MetricCard("Avg Consumption", "0 L", "Per day", COLORS["accent"])
        self.card_abnormal = MetricCard("Abnormal", "0", "Need attention", COLORS["danger"])
        self.card_status = MetricCard("Overall Status", "—", "System health", COLORS["success"])
        for c in (self.card_total, self.card_avg, self.card_abnormal, self.card_status):
            cards.addWidget(c)
        layout.addLayout(cards)

        mid = QHBoxLayout()
        mid.setSpacing(14)

        pie_card = QFrame()
        pie_card.setObjectName("card")
        pie_card.setStyleSheet(f"#card {{ background: white; border-radius: 14px; border: 1px solid {COLORS['border']}; }}")
        apply_shadow(pie_card)
        pie_layout = QVBoxLayout(pie_card)
        pie_layout.setContentsMargins(16, 14, 16, 14)
        pie_title = QLabel("Quality Status Distribution")
        pie_title.setStyleSheet(f"font-weight: 700; color: {COLORS['text']}; font-size: 14px;")
        pie_layout.addWidget(pie_title)

        self.pie_series = QPieSeries()
        self.pie_chart = QChart()
        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.pie_chart.legend().setAlignment(Qt.AlignRight)
        self.pie_chart.setBackgroundVisible(False)
        pie_view = QChartView(self.pie_chart)
        pie_view.setRenderHint(QPainter.Antialiasing)
        pie_view.setMinimumHeight(220)
        pie_layout.addWidget(pie_view)
        mid.addWidget(pie_card, 1)

        bar_card = QFrame()
        bar_card.setObjectName("card")
        bar_card.setStyleSheet(f"#card {{ background: white; border-radius: 14px; border: 1px solid {COLORS['border']}; }}")
        apply_shadow(bar_card)
        bar_layout = QVBoxLayout(bar_card)
        bar_layout.setContentsMargins(16, 14, 16, 14)
        bar_title = QLabel("Avg Consumption by Location (L)")
        bar_title.setStyleSheet(f"font-weight: 700; color: {COLORS['text']}; font-size: 14px;")
        bar_layout.addWidget(bar_title)

        self.bar_series = QBarSeries()
        self.bar_chart = QChart()
        self.bar_chart.addSeries(self.bar_series)
        self.bar_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.bar_chart.legend().setVisible(False)
        self.bar_chart.setBackgroundVisible(False)
        self.bar_axis_x = QBarCategoryAxis()
        self.bar_axis_y = QValueAxis()
        self.bar_chart.addAxis(self.bar_axis_x, Qt.AlignBottom)
        self.bar_chart.addAxis(self.bar_axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(self.bar_axis_x)
        self.bar_series.attachAxis(self.bar_axis_y)
        bar_view = QChartView(self.bar_chart)
        bar_view.setRenderHint(QPainter.Antialiasing)
        bar_view.setMinimumHeight(220)
        bar_layout.addWidget(bar_view)
        mid.addWidget(bar_card, 1)

        layout.addLayout(mid)

        alert_card = QFrame()
        alert_card.setObjectName("card")
        alert_card.setStyleSheet(f"#card {{ background: white; border-radius: 14px; border: 1px solid {COLORS['border']}; }}")
        apply_shadow(alert_card)
        alert_layout = QVBoxLayout(alert_card)
        alert_layout.setContentsMargins(16, 12, 16, 12)
        alert_title = QLabel("Recent Alerts")
        alert_title.setStyleSheet(f"font-weight: 700; color: {COLORS['text']}; font-size: 14px;")
        alert_layout.addWidget(alert_title)
        self.alert_list = QLabel("No alerts")
        self.alert_list.setWordWrap(True)
        self.alert_list.setStyleSheet(f"color: {COLORS['muted']}; font-size: 12px;")
        alert_layout.addWidget(self.alert_list)
        layout.addWidget(alert_card)

        return page

    def _refresh_dashboard(self) -> None:
        total = len(self.readings)
        abnormal = sum(1 for r in self.readings if r.is_abnormal())
        avg = sum(r.consumption for r in self.readings) / total if total else 0
        status = "ATTENTION" if abnormal else "HEALTHY"

        self.card_total.update_value(str(total), "All locations")
        self.card_avg.update_value(f"{avg:.0f} L", "Per day")
        self.card_abnormal.update_value(str(abnormal), "Need attention")
        self.card_status.update_value(status, "System health")

        self.pie_series.clear()
        if total:
            s1 = self.pie_series.append("Normal", total - abnormal)
            s1.setColor(QColor(COLORS["success"]))
            s1.setLabelVisible(True)
            s2 = self.pie_series.append("Abnormal", abnormal)
            s2.setColor(QColor(COLORS["danger"]))
            s2.setLabelVisible(True)

        self.bar_series.clear()
        loc_map: dict[str, list[float]] = {}
        for r in self.readings:
            loc_map.setdefault(r.location.name, []).append(r.consumption)
        if loc_map:
            bar_set = QBarSet("Avg L")
            bar_set.setColor(QColor(COLORS["primary"]))
            cats = []
            for name, vals in loc_map.items():
                cats.append(name[:12])
                bar_set.append(sum(vals) / len(vals))
            self.bar_series.append(bar_set)
            self.bar_axis_x.clear()
            self.bar_axis_x.append(cats)
            self.bar_axis_y.setRange(0, max(bar_set) * 1.2 if len(bar_set) else 100)

        all_alerts = []
        for r in sorted(self.readings, key=lambda x: x.reading_date, reverse=True):
            for a in r.get_alerts():
                all_alerts.append(f"• {r.reading_date} | {r.location.name}: {a}")
        if all_alerts:
            self.alert_list.setText("\n".join(all_alerts[:8]))
            self.alert_list.setStyleSheet(f"color: {COLORS['danger']}; font-size: 12px;")
        else:
            self.alert_list.setText("✓ No abnormal readings at the moment.")
            self.alert_list.setStyleSheet(f"color: {COLORS['success']}; font-size: 12px;")

    # -------------------- ADD READING --------------------
    def _create_add_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet(f"#card {{ background: white; border-radius: 16px; border: 1px solid {COLORS['border']}; }}")
        apply_shadow(card)
        card.setMaximumWidth(520)
        form = QVBoxLayout(card)
        form.setContentsMargins(28, 24, 28, 24)
        form.setSpacing(12)

        form.addWidget(QLabel("<b style='font-size:15px;'>Record New Water Reading</b>"))

        self.in_loc = QLineEdit()
        self.in_loc.setPlaceholderText("Location name (e.g. Green Villa)")
        form.addWidget(QLabel("Location Name"))
        form.addWidget(self.in_loc)

        self.in_addr = QLineEdit()
        self.in_addr.setPlaceholderText("Address")
        form.addWidget(QLabel("Address"))
        form.addWidget(self.in_addr)

        self.in_type = QComboBox()
        self.in_type.addItems(["Household", "School", "Community", "Other"])
        form.addWidget(QLabel("Location Type"))
        form.addWidget(self.in_type)

        self.in_user = QLineEdit()
        self.in_user.setPlaceholderText("Recorded by (name)")
        form.addWidget(QLabel("Recorded By"))
        form.addWidget(self.in_user)

        self.in_date = QDateEdit()
        self.in_date.setCalendarPopup(True)
        self.in_date.setDate(QDate.currentDate())
        form.addWidget(QLabel("Date"))
        form.addWidget(self.in_date)

        self.in_cons = QDoubleSpinBox()
        self.in_cons.setRange(0, 50000)
        self.in_cons.setSuffix(" L")
        self.in_cons.setValue(300)
        form.addWidget(QLabel("Daily Consumption (Litres)"))
        form.addWidget(self.in_cons)

        self.in_ph = QDoubleSpinBox()
        self.in_ph.setRange(0, 14)
        self.in_ph.setSingleStep(0.1)
        self.in_ph.setDecimals(1)
        self.in_ph.setValue(7.0)
        form.addWidget(QLabel("pH Value"))
        form.addWidget(self.in_ph)

        self.in_turb = QDoubleSpinBox()
        self.in_turb.setRange(0, 100)
        self.in_turb.setSingleStep(0.1)
        self.in_turb.setDecimals(1)
        self.in_turb.setValue(2.0)
        self.in_turb.setSuffix(" NTU")
        form.addWidget(QLabel("Turbidity"))
        form.addWidget(self.in_turb)

        form.addSpacing(8)
        btn_row = QHBoxLayout()
        btn_add = QPushButton("➕  Add Reading")
        btn_add.setObjectName("primaryBtn")
        btn_add.setCursor(Qt.PointingHandCursor)
        btn_add.clicked.connect(self._on_add_reading)
        btn_row.addWidget(btn_add)

        btn_clear = QPushButton("Clear Form")
        btn_clear.setObjectName("secondaryBtn")
        btn_clear.clicked.connect(self._clear_form)
        btn_row.addWidget(btn_clear)
        form.addLayout(btn_row)

        layout.addWidget(card, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addStretch()
        return page

    def _on_add_reading(self) -> None:
        name = self.in_loc.text().strip()
        user_name = self.in_user.text().strip()
        if not name or not user_name:
            QMessageBox.warning(self, "Missing Data", "Please fill Location and User name.")
            return

        loc = Location(name, self.in_addr.text().strip() or "N/A", self.in_type.currentText())
        user = User(f"U{len(self.readings)+1:03d}", user_name)
        r_date = self.in_date.date().toPython()
        reading = WaterReading(r_date, loc, user, self.in_cons.value(), self.in_ph.value(), self.in_turb.value())
        self.readings.append(reading)
        self._refresh_all()

        status = "ABNORMAL ⚠" if reading.is_abnormal() else "Normal ✓"
        QMessageBox.information(self, "Reading Added",
            f"Reading recorded successfully!\n\nStatus: {status}\nAlerts: {', '.join(reading.get_alerts()) or 'None'}")
        self._clear_form()

    def _clear_form(self) -> None:
        self.in_loc.clear()
        self.in_addr.clear()
        self.in_user.clear()
        self.in_date.setDate(QDate.currentDate())
        self.in_cons.setValue(300)
        self.in_ph.setValue(7.0)
        self.in_turb.setValue(2.0)

    # -------------------- ALL READINGS --------------------
    def _create_list_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Date", "Location", "Type", "User", "Consumption (L)", "pH", "Turbidity", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        return page

    def _refresh_table(self) -> None:
        self.table.setRowCount(0)
        for r in sorted(self.readings, key=lambda x: x.reading_date, reverse=True):
            row = self.table.rowCount()
            self.table.insertRow(row)
            values = [
                str(r.reading_date), r.location.name, r.location.location_type,
                r.recorded_by.name, f"{r.consumption:.1f}", f"{r.ph:.1f}",
                f"{r.turbidity:.1f}", r.quality_status()
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                if col == 7:
                    if val == "ABNORMAL":
                        item.setForeground(QColor(COLORS["danger"]))
                        item.setFont(QFont("Segoe UI", 10, QFont.Bold))
                    else:
                        item.setForeground(QColor(COLORS["success"]))
                self.table.setItem(row, col, item)

    # -------------------- REPORT --------------------
    def _create_report_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        top = QHBoxLayout()
        top.addWidget(QLabel("Select Location:"))
        self.report_loc_combo = QComboBox()
        self.report_loc_combo.setMinimumWidth(220)
        top.addWidget(self.report_loc_combo)
        btn_gen = QPushButton("📊  Generate Report")
        btn_gen.setObjectName("primaryBtn")
        btn_gen.setCursor(Qt.PointingHandCursor)
        btn_gen.clicked.connect(self._generate_report)
        top.addWidget(btn_gen)
        top.addStretch()
        layout.addLayout(top)

        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setStyleSheet(f"""
            QTextEdit {{
                background: white;
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
                padding: 16px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12.5px;
                color: {COLORS['text']};
            }}
        """)
        layout.addWidget(self.report_text)
        return page

    def _populate_report_locations(self) -> None:
        self.report_loc_combo.clear()
        locs = sorted({r.location.name for r in self.readings})
        self.report_loc_combo.addItems(locs)

    def _generate_report(self) -> None:
        loc_name = self.report_loc_combo.currentText()
        if not loc_name:
            QMessageBox.warning(self, "No Data", "No locations available.")
            return
        sample = next((r for r in self.readings if r.location.name == loc_name), None)
        if not sample:
            return
        report = MonitoringReport(f"AG-{datetime.now().strftime('%Y%m%d-%H%M')}", sample.recorded_by, sample.location)
        for r in self.readings:
            if r.location.name == loc_name:
                report.add_reading(r)
        self.report_text.setPlainText(report.generate_text())

    # -------------------- ABOUT --------------------
    def _create_about_page(self) -> QWidget:
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet(f"background: white; border-radius: 16px; border: 1px solid {COLORS['border']};")
        apply_shadow(card)
        v = QVBoxLayout(card)
        v.setContentsMargins(28, 24, 28, 24)
        v.setSpacing(10)

        v.addWidget(QLabel("<b style='font-size:18px;'>AquaGuard</b>"))
        v.addWidget(QLabel("Community Water Quality & Usage Monitor<br>HACK-AI-THON 2026 • National Level Project"))
        v.addSpacing(8)
        v.addWidget(QLabel("<b>SDG Alignment</b>"))
        v.addWidget(QLabel("• SDG 6 – Clean Water and Sanitation<br>• SDG 12 – Responsible Consumption and Production"))
        v.addSpacing(8)
        v.addWidget(QLabel("<b>Core OOP Classes</b>"))
        v.addWidget(QLabel("• Location / User<br>• WaterReading (with threshold checks)<br>• MonitoringReport (trends, alerts, recommendations)"))
        v.addSpacing(8)
        v.addWidget(QLabel("<b>Thresholds</b>"))
        v.addWidget(QLabel("• pH : 6.5 – 8.5<br>• Turbidity : ≤ 5.0 NTU<br>• Daily Consumption : ≤ 450 L (alert)"))
        v.addSpacing(8)
        v.addWidget(QLabel("<i>Built with Python + PySide6 • Demonstrates Python fundamentals & OOP</i>"))
        v.addStretch()
        layout.addWidget(card)
        return page

    def _refresh_all(self) -> None:
        self._refresh_dashboard()
        self._refresh_table()
        self._populate_report_locations()


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AquaGuardApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
