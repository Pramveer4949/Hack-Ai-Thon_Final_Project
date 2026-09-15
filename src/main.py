from __future__ import annotations
import sys
from datetime import date, datetime
from typing import List
from PySide6.QtCore import Qt, QRectF, QDate
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import (QApplication,QFrame,QGridLayout,QHBoxLayout,QHeaderView,QLabel,
    QLineEdit,QMainWindow,QMessageBox,QPushButton,QStackedWidget,QTableWidget,QTableWidgetItem,
    QVBoxLayout,QWidget,QComboBox,QDateEdit,QDoubleSpinBox)

# ========================= OOP / DATA MODEL =========================
class Location:
    def __init__(self, name: str, address: str, location_type: str = "Household"):
        self.name, self.address, self.location_type = name, address, location_type
    def __str__(self): return f"{self.name} ({self.location_type})"

class User:
    def __init__(self, user_id: str, name: str, role: str = "Resident"):
        self.user_id, self.name, self.role = user_id, name, role
    def __str__(self): return self.name

class WaterReading:
    PH_MIN, PH_MAX = 6.5, 8.5
    TURBIDITY_LIMIT = 5.0
    CONSUMPTION_LIMIT = 450.0
    def __init__(self, reading_date, location, recorded_by, consumption, ph, turbidity):
        self.reading_date=reading_date; self.location=location; self.recorded_by=recorded_by
        self.consumption=consumption; self.ph=ph; self.turbidity=turbidity
    def get_alerts(self) -> List[str]:
        a=[]
        if self.ph < self.PH_MIN: a.append(f"Low pH: {self.ph:.1f}")
        elif self.ph > self.PH_MAX: a.append(f"High pH: {self.ph:.1f}")
        if self.turbidity > self.TURBIDITY_LIMIT: a.append(f"High turbidity: {self.turbidity:.1f} NTU")
        if self.consumption > self.CONSUMPTION_LIMIT: a.append(f"High consumption: {self.consumption:.0f} L/day")
        return a
    def is_abnormal(self): return bool(self.get_alerts())

class MonitoringReport:
    def __init__(self, report_id, generated_by, location):
        self.report_id=report_id; self.generated_by=generated_by; self.location=location
        self.readings=[]; self.generated_at=datetime.now()
    def add_reading(self, reading): self.readings.append(reading)
    def average_consumption(self):
        return sum(r.consumption for r in self.readings)/len(self.readings) if self.readings else 0
    def consumption_trend(self):
        if len(self.readings)<2: return "Insufficient data"
        s=sorted(self.readings,key=lambda r:r.reading_date); first,last=s[0].consumption,s[-1].consumption
        if last > first*1.15: return "Increasing"
        if last < first*0.85: return "Decreasing"
        return "Stable"
    def status(self): return "ATTENTION NEEDED" if any(r.is_abnormal() for r in self.readings) else "NORMAL"
    def all_alerts(self):
        out=[]
        for r in sorted(self.readings,key=lambda x:x.reading_date):
            for a in r.get_alerts(): out.append(f"{r.reading_date.isoformat()} • {a}")
        return out
    def recommendations(self):
        rec=[]; avg=self.average_consumption(); trend=self.consumption_trend(); alerts=" ".join(self.all_alerts()).lower()
        if avg>400: rec.append("Reduce daily water use and check taps, toilets and unnecessary usage.")
        if trend=="Increasing": rec.append("Consumption is rising; monitor the next few days and investigate the cause.")
        if "turbidity" in alerts: rec.append("Inspect the water source/filter because turbidity is above the defined limit.")
        if "ph" in alerts: rec.append("Review the water-quality observation and consider further testing.")
        if not rec: rec=["Water usage and observed quality are within the project's defined limits.","Continue regular monitoring and responsible water conservation."]
        return rec

# ========================= SAMPLE DATA =========================
def sample_data():
    a=Location("Green Villa","Sector 12, Noida"); b=Location("Sunrise Apt","Block B, Delhi")
    u1=User("U101","Priya Sharma"); u2=User("U102","Rahul Verma")
    return [
        WaterReading(date(2026,9,8),a,u1,310,7.2,2.1), WaterReading(date(2026,9,9),a,u1,325,7.3,2.4),
        WaterReading(date(2026,9,10),a,u1,480,7.1,2.8), WaterReading(date(2026,9,11),a,u1,510,7.0,3.2),
        WaterReading(date(2026,9,8),b,u2,280,7.4,1.9), WaterReading(date(2026,9,9),b,u2,295,7.4,2.0),
        WaterReading(date(2026,9,10),b,u2,300,7.3,2.2)]

# ========================= CUSTOM VISUALS =========================
class StatCard(QFrame):
    def __init__(self,title,value,sub,accent,icon):
        super().__init__(); self.setObjectName("card")
        l=QVBoxLayout(self); l.setContentsMargins(16,14,16,12); l.setSpacing(4)
        row=QHBoxLayout(); ic=QLabel(icon); ic.setAlignment(Qt.AlignCenter); ic.setFixedSize(42,42)
        ic.setStyleSheet(f"background:{accent};color:white;border-radius:21px;font-size:19px;font-weight:800;")
        t=QLabel(title); t.setObjectName("cardTitle"); row.addWidget(ic); row.addSpacing(9); row.addWidget(t); row.addStretch()
        self.value=QLabel(value); self.value.setObjectName("cardValue"); self.sub=QLabel(sub); self.sub.setObjectName("cardSub")
        l.addLayout(row); l.addWidget(self.value); l.addWidget(self.sub)

class DonutChart(QWidget):
    def __init__(self): super().__init__(); self.setMinimumHeight(245); self.values=[60,30,6,4]; self.labels=["Green Villa","Sunrise Apt","Other","Community"]; self.colors=["#20D477","#249DE8","#FFB52F","#8B5CF6"]
    def paintEvent(self,e):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing); cx,cy=105,self.height()//2; r=73; rect=QRectF(cx-r,cy-r,2*r,2*r); start=0; total=sum(self.values)
        for v,c in zip(self.values,self.colors):
            span=int(360*v/total*16); p.setPen(Qt.NoPen); p.setBrush(QColor(c)); p.drawPie(rect,start,span); start+=span
        p.setBrush(QColor("#F6FBFD")); p.drawEllipse(QRectF(cx-41,cy-41,82,82)); p.setPen(QColor("#123E68")); p.setFont(QFont("Segoe UI",10,QFont.Bold)); p.drawText(QRectF(cx-38,cy-16,76,32),Qt.AlignCenter,"Usage\nshare")
        y=cy-54; p.setFont(QFont("Segoe UI",9))
        for v,l,c in zip(self.values,self.labels,self.colors):
            p.setBrush(QColor(c)); p.drawEllipse(QRectF(200,y+3,10,10)); p.setPen(QColor("#315C79")); p.drawText(218,y+13,l); p.setPen(QColor("#123E68")); p.setFont(QFont("Segoe UI",9,QFont.Bold)); p.drawText(315,y+13,f"{v}%"); p.setFont(QFont("Segoe UI",9)); y+=34

class BarChart(QWidget):
    def __init__(self): super().__init__(); self.setMinimumHeight(245); self.values=[510,300,325,280]; self.labels=["Green Villa","Sunrise Apt","Sep 9","Sep 8"]; self.colors=["#20D477","#40A8EF","#FFBB42","#9365EE"]
    def paintEvent(self,e):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing); left,bottom,top=42,self.height()-42,24; h=bottom-top; mx=max(self.values)*1.15
        p.setPen(QPen(QColor("#D9EAF2"),1))
        for i in range(5):
            y=bottom-i*h/4; p.drawLine(left,int(y),self.width()-18,int(y))
        x=65
        for v,l,c in zip(self.values,self.labels,self.colors):
            bh=h*v/mx; y=bottom-bh; p.setPen(Qt.NoPen); p.setBrush(QColor(c)); p.drawRoundedRect(QRectF(x,y,43,bh),8,8)
            p.setPen(QColor("#123E68")); p.setFont(QFont("Segoe UI",9,QFont.Bold)); p.drawText(QRectF(x-10,y-21,63,18),Qt.AlignCenter,str(v)); p.setFont(QFont("Segoe UI",8)); p.drawText(QRectF(x-22,bottom+6,87,30),Qt.AlignCenter|Qt.TextWordWrap,l); x+=75

class Section(QFrame):
    def __init__(self,title,sub=""):
        super().__init__(); self.setObjectName("section"); self.l=QVBoxLayout(self); self.l.setContentsMargins(16,14,16,14); self.l.setSpacing(9)
        row=QHBoxLayout(); t=QLabel(title); t.setObjectName("sectionTitle"); row.addWidget(t); row.addStretch()
        if sub: s=QLabel(sub); s.setObjectName("sectionSub"); row.addWidget(s)
        self.l.addLayout(row)

# ========================= MAIN GUI =========================
class AquaGuardApp(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("AquaGuard AI • Community Water Monitor"); self.resize(1400,850); self.setMinimumSize(1150,720)
        self.readings=sample_data(); self.style(); self.build(); self.refresh()
    def style(self):
        self.setStyleSheet('''
        QMainWindow,QWidget{background:#F2FAFC;color:#123E68;font-family:"Segoe UI";}
        QFrame#sidebar,QFrame#header,QFrame#card,QFrame#section{background:#FFFFFF;border:1px solid #E0EEF3;border-radius:20px;}
        QLabel#brand{color:#087A51;font-size:24px;font-weight:800;} QLabel#small{color:#718A9A;font-size:10px;}
        QLabel#pageTitle{color:#087A51;font-size:27px;font-weight:800;} QLabel#pageSub{color:#6B8798;font-size:11px;}
        QLabel#cardTitle{color:#245675;font-size:11px;} QLabel#cardValue{color:#0B3C69;font-size:24px;font-weight:800;} QLabel#cardSub{color:#25A66A;font-size:10px;}
        QLabel#sectionTitle{color:#123E68;font-size:16px;font-weight:800;} QLabel#sectionSub{color:#7891A0;font-size:10px;}
        QPushButton#nav{background:transparent;border:none;border-radius:12px;color:#19557E;text-align:left;padding:11px 12px;font-size:12px;}
        QPushButton#nav:hover,QPushButton#nav[active="true"]{background:#B9F4DA;color:#087A51;font-weight:700;}
        QPushButton#primary{background:#13B66A;color:white;border:none;border-radius:11px;padding:10px 17px;font-weight:700;}
        QPushButton#secondary{background:#E7F3F8;color:#16557F;border:none;border-radius:11px;padding:10px 17px;font-weight:700;}
        QLineEdit{background:#F7FBFD;border:1px solid #D4E7EF;border-radius:10px;padding:9px;color:#123E68;} QLineEdit:focus{border:2px solid #57D99D;}
        QTableWidget{background:#FFFFFF;border:none;gridline-color:#E8F1F5;border-radius:10px;} QHeaderView::section{background:#E8F5FA;color:#174B72;border:none;padding:8px;font-weight:700;}
        ''')
    def build(self):
        root=QHBoxLayout(); root.setContentsMargins(16,16,16,16); root.setSpacing(12); w=QWidget(); w.setLayout(root); self.setCentralWidget(w)
        root.addWidget(self.sidebar());
        content=QWidget(); cl=QVBoxLayout(content); cl.setContentsMargins(0,0,0,0); cl.setSpacing(10); cl.addWidget(self.header())
        self.stack=QStackedWidget(); self.stack.addWidget(self.dashboard()); self.stack.addWidget(self.addpage()); self.stack.addWidget(self.analysis()); self.stack.addWidget(self.reportpage()); cl.addWidget(self.stack); root.addWidget(content,1)
    def sidebar(self):
        s=QFrame(); s.setObjectName("sidebar"); s.setFixedWidth(225); l=QVBoxLayout(s); l.setContentsMargins(15,18,15,15)
        top=QHBoxLayout(); logo=QLabel("✓"); logo.setAlignment(Qt.AlignCenter); logo.setFixedSize(46,46); logo.setStyleSheet("background:#20C978;color:white;border-radius:23px;font-size:22px;font-weight:800;")
        b=QVBoxLayout(); brand=QLabel("AquaGuard"); brand.setObjectName("brand"); sm=QLabel("Water • Quality • Conservation"); sm.setObjectName("small"); b.addWidget(brand); b.addWidget(sm); top.addWidget(logo); top.addSpacing(8); top.addLayout(b); l.addLayout(top); l.addSpacing(20)
        self.nav={}; items=[("⌂","Dashboard"),("＋","Add Reading"),("▥","Water Analysis"),("↗","Monitoring Report")]
        for icon,name in items:
            q=QPushButton(f"  {icon}    {name}"); q.setObjectName("nav"); q.setProperty("active",name=="Dashboard"); q.clicked.connect(lambda _,n=name:self.go(n)); l.addWidget(q); self.nav[name]=q
        l.addStretch(); box=QFrame(); box.setStyleSheet("QFrame{background:#ECFBF4;border:1px solid #C8F1DD;border-radius:17px;}")
        bl=QVBoxLayout(box); a=QLabel("SDG 6  •  Clean Water"); a.setStyleSheet("color:#087A51;font-weight:800;font-size:12px;"); c=QLabel("SDG 12  •  Responsible Consumption"); c.setStyleSheet("color:#D17B16;font-weight:800;font-size:12px;"); bl.addWidget(a); bl.addWidget(c); l.addWidget(box)
        f=QLabel("Python + OOP + PySide6\nFunctional Prototype"); f.setAlignment(Qt.AlignCenter); f.setStyleSheet("color:#8AA0AE;font-size:9px;padding:8px;"); l.addWidget(f); return s
    def header(self):
        h=QFrame(); h.setObjectName("header"); h.setMinimumHeight(82); l=QHBoxLayout(h); l.setContentsMargins(18,10,18,10); box=QVBoxLayout(); t=QLabel("AquaGuard"); t.setObjectName("pageTitle"); sub=QLabel("Track. Understand. Conserve. Build a safer water future."); sub.setObjectName("pageSub"); box.addWidget(t); box.addWidget(sub); l.addLayout(box); l.addStretch(); d=QLabel(datetime.now().strftime("%A, %d %B %Y")); d.setStyleSheet("font-size:11px;font-weight:600;color:#174D77;"); l.addWidget(d); p=QLabel(" P "); p.setAlignment(Qt.AlignCenter); p.setStyleSheet("background:#DFF1FB;color:#1673B8;border-radius:18px;font-weight:800;padding:8px;"); l.addWidget(p); return h
    def dashboard(self):
        p=QWidget(); l=QVBoxLayout(p); l.setContentsMargins(0,0,0,0); l.setSpacing(10); g=QGridLayout(); g.setSpacing(9)
        self.avg=StatCard("Average Daily Consumption","—","Across recorded readings","#20C978","💧"); self.total=StatCard("Total Recorded Use","—","All demo readings","#269DE8","≋"); self.alert=StatCard("Active Alerts","—","Quality + usage checks","#F15B6A","!"); self.status=StatCard("Water Safety Status","—","Defined project thresholds","#8B5CF6","✓")
        for i,c in enumerate([self.avg,self.total,self.alert,self.status]): g.addWidget(c,0,i)
        l.addLayout(g); row=QHBoxLayout(); a=Section("Consumption Overview","Location-wise"); a.l.addWidget(DonutChart()); b=Section("Usage Comparison","Latest demo values"); b.l.addWidget(BarChart()); row.addWidget(a,1); row.addWidget(b,1); l.addLayout(row)
        bot=QHBoxLayout(); t=Section("Recent Water Readings","Live prototype data"); self.recent=self.table(["Date","Location","Consumption","pH","Turbidity","Status"]); t.l.addWidget(self.recent); bot.addWidget(t,2); q=Section("Quick Insights","System-generated"); self.ins=QLabel(); self.ins.setWordWrap(True); self.ins.setStyleSheet("color:#416C84;font-size:11px;padding:7px;line-height:150%;"); q.l.addWidget(self.ins); bot.addWidget(q,1); l.addLayout(bot,1); return p
    def addpage(self):
        p=QWidget(); l=QVBoxLayout(p); l.setContentsMargins(0,0,0,0); l.setSpacing(12)

        intro=QFrame(); intro.setStyleSheet("QFrame{background:#E9FBF3;border:1px solid #C9F0DD;border-radius:18px;}")
        il=QHBoxLayout(intro); il.setContentsMargins(16,12,16,12)
        ic=QLabel("💧"); ic.setAlignment(Qt.AlignCenter); ic.setFixedSize(42,42); ic.setStyleSheet("background:#18C778;color:white;border-radius:21px;font-size:20px;")
        ib=QVBoxLayout(); t=QLabel("Record a new water reading"); t.setStyleSheet("font-size:16px;font-weight:800;color:#087A51;"); st=QLabel("Enter the observation below. AquaGuard automatically checks the defined project thresholds."); st.setStyleSheet("font-size:10px;color:#4D7B69;"); ib.addWidget(t); ib.addWidget(st); il.addWidget(ic); il.addSpacing(10); il.addLayout(ib); il.addStretch(); l.addWidget(intro)

        identity=Section("1  •  Location & Recorder","Who and where is being monitored?"); g=QGridLayout(); g.setHorizontalSpacing(12); g.setVerticalSpacing(8)
        self.le_loc=QLineEdit(); self.le_loc.setPlaceholderText("e.g. Green Villa")
        self.le_addr=QLineEdit(); self.le_addr.setPlaceholderText("e.g. Sector 12, Noida")
        self.le_user=QLineEdit(); self.le_user.setPlaceholderText("e.g. Priya Sharma")
        self.location_type=QComboBox(); self.location_type.addItems(["Household","School","Community"])
        for lab,w,r,c in [("Location name",self.le_loc,0,0),("Location type",self.location_type,0,2),("Address",self.le_addr,1,0),("Recorded by",self.le_user,1,2)]:
            z=QLabel(lab); z.setStyleSheet("font-size:10px;font-weight:700;color:#416B84;"); g.addWidget(z,r,c); g.addWidget(w,r,c+1)
        identity.l.addLayout(g); l.addWidget(identity)

        measurements=Section("2  •  Water Measurements","Daily usage + basic quality observations")
        g2=QGridLayout(); g2.setHorizontalSpacing(12); g2.setVerticalSpacing(8)
        self.le_date=QDateEdit(); self.le_date.setCalendarPopup(True); self.le_date.setDate(QDate.currentDate()); self.le_date.setDisplayFormat("dd MMM yyyy")
        self.le_cons=QDoubleSpinBox(); self.le_cons.setRange(0,100000); self.le_cons.setDecimals(1); self.le_cons.setSuffix(" L/day"); self.le_cons.setSpecialValueText("Enter consumption…")
        self.le_ph=QDoubleSpinBox(); self.le_ph.setRange(0,14); self.le_ph.setDecimals(1); self.le_ph.setSingleStep(.1); self.le_ph.setSpecialValueText("Enter pH…")
        self.le_turb=QDoubleSpinBox(); self.le_turb.setRange(0,10000); self.le_turb.setDecimals(1); self.le_turb.setSuffix(" NTU"); self.le_turb.setSpecialValueText("Enter turbidity…")
        for lab,w,r,c in [("Reading date",self.le_date,0,0),("Daily consumption",self.le_cons,0,2),("pH value",self.le_ph,1,0),("Turbidity",self.le_turb,1,2)]:
            z=QLabel(lab); z.setStyleSheet("font-size:10px;font-weight:700;color:#416B84;"); g2.addWidget(z,r,c); g2.addWidget(w,r,c+1)
        measurements.l.addLayout(g2)
        note=QLabel("PROJECT THRESHOLDS   •   pH: 6.5–8.5   •   Turbidity: ≤ 5 NTU   •   Consumption: ≤ 450 L/day")
        note.setStyleSheet("background:#EFF8FC;color:#39708D;border-radius:10px;padding:9px;font-size:10px;font-weight:600;"); measurements.l.addWidget(note); l.addWidget(measurements)

        actions=QFrame(); actions.setStyleSheet("QFrame{background:#FFFFFF;border:1px solid #E1EEF3;border-radius:18px;}"); al=QHBoxLayout(actions); al.setContentsMargins(14,10,14,10)
        self.form_status=QLabel("Ready to record a reading"); self.form_status.setStyleSheet("color:#6A879A;font-size:10px;")
        clr=QPushButton("↺  Reset Form"); clr.setObjectName("secondary"); clr.clicked.connect(self.clear)
        add=QPushButton("＋  Record Water Reading"); add.setObjectName("primary"); add.setMinimumHeight(40); add.clicked.connect(self.add)
        al.addWidget(self.form_status); al.addStretch(); al.addWidget(clr); al.addWidget(add); l.addWidget(actions); l.addStretch(); return p
    def analysis(self):
        p=QWidget(); l=QVBoxLayout(p); l.setContentsMargins(0,0,0,0); s=Section("Water Analysis","Trend detection and abnormal-reading checks"); self.at=self.table(["Location","Readings","Average L/day","Trend","Status"]); s.l.addWidget(self.at); l.addWidget(s); return p
    def reportpage(self):
        p=QWidget(); l=QVBoxLayout(p); l.setContentsMargins(0,0,0,0); s=Section("Monitoring Report","Consumption • quality status • alerts • trends • recommendations"); self.rt=QLabel(); self.rt.setStyleSheet("font-size:15px;font-weight:800;color:#0D4A75;"); s.l.addWidget(self.rt); self.rtab=self.table(["Date","Consumption","pH","Turbidity","Status","Alerts"]); s.l.addWidget(self.rtab); self.rtext=QLabel(); self.rtext.setWordWrap(True); self.rtext.setStyleSheet("background:#F1FAF6;color:#315E50;border-radius:13px;padding:13px;font-size:11px;"); s.l.addWidget(self.rtext); b=QPushButton("⟳  Generate / Refresh Report"); b.setObjectName("primary"); b.clicked.connect(self.report); s.l.addWidget(b); l.addWidget(s); return p
    def table(self,headers):
        t=QTableWidget(); t.setColumnCount(len(headers)); t.setHorizontalHeaderLabels(headers); t.verticalHeader().setVisible(False); t.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); t.setEditTriggers(QTableWidget.NoEditTriggers); t.setSelectionBehavior(QTableWidget.SelectRows); t.setMinimumHeight(210); return t
    def go(self,name):
        idx={"Dashboard":0,"Add Reading":1,"Water Analysis":2,"Monitoring Report":3}[name]; self.stack.setCurrentIndex(idx)
        for n,b in self.nav.items(): b.setProperty("active",n==name); b.style().unpolish(b); b.style().polish(b)
        if name=="Water Analysis": self.analysis_refresh()
        if name=="Monitoring Report": self.report()
    def add(self):
        try:
            loc=self.le_loc.text().strip(); user=self.le_user.text().strip(); addr=self.le_addr.text().strip()
            if not loc: self.le_loc.setFocus(); raise ValueError("Please enter a location name.")
            if not user: self.le_user.setFocus(); raise ValueError("Please enter the recorder name.")
            q=self.le_date.date(); dt=date(q.year(),q.month(),q.day())
            cons=self.le_cons.value(); ph=self.le_ph.value(); turb=self.le_turb.value()
            if cons<=0: self.le_cons.setFocus(); raise ValueError("Please enter daily consumption greater than 0.")
            if ph<=0: self.le_ph.setFocus(); raise ValueError("Please enter a valid pH value greater than 0.")
            if turb<=0: self.le_turb.setFocus(); raise ValueError("Please enter turbidity greater than 0.")
            r=WaterReading(dt,Location(loc,addr or "Not provided",self.location_type.currentText()),User("U-DEMO",user),cons,ph,turb); self.readings.append(r); self.clear(); self.refresh(); self.analysis_refresh(); self.report()
            if r.is_abnormal():
                self.form_status.setText("⚠ Reading recorded — attention is needed.")
                QMessageBox.warning(self,"Reading Recorded • Attention Needed","The reading was saved successfully, but AquaGuard detected:\n\n"+"\n".join("• "+x for x in r.get_alerts()))
            else:
                self.form_status.setText("✓ Reading recorded successfully.")
                QMessageBox.information(self,"Reading Recorded","Reading saved successfully. No abnormal conditions were detected.")
        except ValueError as e:
            self.form_status.setText("⚠ Please check the form.")
            QMessageBox.warning(self,"Check the Form",str(e))
    def clear(self):
        self.le_cons.setValue(0); self.le_ph.setValue(0); self.le_turb.setValue(0); self.le_date.setDate(QDate.currentDate())
        if hasattr(self,"form_status"): self.form_status.setText("Ready to record a reading")
    def refresh(self):
        if not self.readings:return
        total=sum(r.consumption for r in self.readings); avg=total/len(self.readings); alerts=sum(len(r.get_alerts()) for r in self.readings); abnormal=any(r.is_abnormal() for r in self.readings)
        self.avg.value.setText(f"{avg:,.0f} L/day"); self.total.value.setText(f"{total:,.0f} L"); self.alert.value.setText(str(alerts)); self.status.value.setText("ATTENTION" if abnormal else "NORMAL")
        self.recent.setRowCount(0)
        for r in sorted(self.readings,key=lambda x:x.reading_date,reverse=True)[:8]:
            row=self.recent.rowCount(); self.recent.insertRow(row); vals=[r.reading_date.isoformat(),r.location.name,f"{r.consumption:.0f} L",f"{r.ph:.1f}",f"{r.turbidity:.1f}","ATTENTION" if r.is_abnormal() else "NORMAL"]
            for c,v in enumerate(vals): self.recent.setItem(row,c,QTableWidgetItem(v))
        latest=max(self.readings,key=lambda r:r.reading_date); self.ins.setText(f"💧 Latest: <b>{latest.location.name}</b> — {latest.consumption:.0f} L/day.<br><br>📈 Trend: <b>{self.trend(latest.location.name)}</b>.<br><br>⚠ Active alerts: <b>{alerts}</b>.<br><br>🌱 Continue regular monitoring and follow generated conservation recommendations.")
    def trend(self,name):
        rs=[r for r in self.readings if r.location.name==name]; rep=MonitoringReport("T",rs[0].recorded_by,rs[0].location)
        for r in rs: rep.add_reading(r)
        return rep.consumption_trend()
    def analysis_refresh(self):
        groups={}
        for r in self.readings: groups.setdefault(r.location.name,[]).append(r)
        self.at.setRowCount(0)
        for name,rs in groups.items():
            rep=MonitoringReport("R",rs[0].recorded_by,rs[0].location)
            for r in rs: rep.add_reading(r)
            row=self.at.rowCount(); self.at.insertRow(row); vals=[name,str(len(rs)),f"{rep.average_consumption():.1f}",rep.consumption_trend(),rep.status()]
            for c,v in enumerate(vals): self.at.setItem(row,c,QTableWidgetItem(v))
    def report(self):
        if not self.readings:return
        name=self.readings[0].location.name; rs=[r for r in self.readings if r.location.name==name]; rep=MonitoringReport("AG-"+datetime.now().strftime("%Y%m%d%H%M"),rs[0].recorded_by,rs[0].location)
        for r in rs: rep.add_reading(r)
        self.rt.setText(f"{rep.location.name} • {rep.location.address}  |  Report {rep.report_id}"); self.rtab.setRowCount(0)
        for r in sorted(rs,key=lambda x:x.reading_date,reverse=True):
            row=self.rtab.rowCount(); self.rtab.insertRow(row); vals=[r.reading_date.isoformat(),f"{r.consumption:.0f} L/day",f"{r.ph:.1f}",f"{r.turbidity:.1f} NTU","ATTENTION" if r.is_abnormal() else "NORMAL",", ".join(r.get_alerts()) or "None"]
            for c,v in enumerate(vals): self.rtab.setItem(row,c,QTableWidgetItem(v))
        alerts=rep.all_alerts(); rec=rep.recommendations(); a="<br>".join("• "+x for x in alerts) if alerts else "• No abnormal readings detected."; rr="<br>".join("• "+x for x in rec)
        self.rtext.setText(f"<b>Average:</b> {rep.average_consumption():.1f} L/day<br><b>Trend:</b> {rep.consumption_trend()}<br><b>Status:</b> {rep.status()}<br><br><b>Alerts</b><br>{a}<br><br><b>Recommended conservation actions</b><br>{rr}")

def main():
    app=QApplication(sys.argv); app.setApplicationName("AquaGuard"); w=AquaGuardApp(); w.show(); sys.exit(app.exec())
if __name__=="__main__": main()
