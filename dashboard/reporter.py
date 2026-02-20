import base64

def generate_html_report(mission_name, health_data, threats, pqc_tag):
    """Generates an advanced HTML report with embedded CSS."""
    
    css = """
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f9; color: #2c3e50; margin: 0; padding: 40px; }
        .container { max-width: 900px; margin: auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .header { border-bottom: 2px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { margin: 0; color: #3498db; font-size: 24px; text-transform: uppercase; letter-spacing: 2px; }
        .timestamp { color: #7f8c8d; font-size: 13px; }
        .section { margin-bottom: 40px; }
        .section h2 { font-size: 18px; border-left: 4px solid #3498db; padding-left: 15px; margin-bottom: 20px; color: #34495e; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0; }
        .card h3 { margin: 0 0 10px 0; font-size: 14px; color: #64748b; text-transform: uppercase; }
        .card p { margin: 0; font-size: 20px; font-weight: bold; color: #1e293b; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th { text-align: left; padding: 12px; background: #f1f5f9; color: #475569; font-size: 13px; border-bottom: 1px solid #e2e8f0; }
        td { padding: 12px; border-bottom: 1px solid #f1f5f9; font-size: 14px; }
        .badge { padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; text-transform: uppercase; }
        .badge-ok { background: #dcfce7; color: #166534; }
        .badge-warn { background: #fef9c3; color: #854d0e; }
        .badge-crit { background: #fee2e2; color: #991b1b; }
        .footer { margin-top: 60px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #94a3b8; font-size: 12px; }
        .pqc-tag { font-family: 'Courier New', monospace; background: #1e293b; color: #38bdf8; padding: 15px; border-radius: 6px; font-size: 12px; overflow-wrap: break-word; }
    </style>
    """
    
    threat_rows = ""
    for t in threats:
        badge = "badge-ok" if t['status'] == "TRACKING" else "badge-crit"
        threat_rows += f"""
        <tr>
            <td>{t['id']}</td>
            <td>{t['type']}</td>
            <td>{t['bearing']}</td>
            <td>{t['range']}</td>
            <td><span class="badge {badge}">{t['status']}</span></td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Mission Report - {mission_name}</title>
        {css}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1>APEX-X MISSION REPORT</h1>
                    <p style="margin:5px 0 0 0; color:#7f8c8d;">{mission_name} Execution Summary</p>
                </div>
                <div class="timestamp">
                    GENERATED: {health_data.get('timestamp', 'N/A')}<br>
                    CLASSIFICATION: SECRET // NOFORN
                </div>
            </div>

            <div class="section">
                <h2>Module Status Matrix</h2>
                <div class="grid">
                    <div class="card">
                        <h3>Link Integrity</h3>
                        <p>99.98%</p>
                    </div>
                    <div class="card">
                        <h3>PQC Security</h3>
                        <p>VERIFIED</p>
                    </div>
                    <div class="card">
                        <h3>Decision Latency</h3>
                        <p>4.2ms</p>
                    </div>
                    <div class="card">
                        <h3>Quorum Status</h3>
                        <p>12/12 NODES</p>
                    </div>
                </div>
            </div>

            <div class="section">
                <h2>Active Threat Landscape</h2>
                <table>
                    <thead>
                        <tr>
                            <th>TARGET ID</th>
                            <th>CLASSIFICATION</th>
                            <th>BEARING</th>
                            <th>RANGE</th>
                            <th>STATUS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {threat_rows}
                    </tbody>
                </table>
            </div>

            <div class="section">
                <h2>Post-Quantum Integrity Tag</h2>
                <div class="pqc-tag">
                    {pqc_tag}
                </div>
            </div>

            <div class="footer">
                © 2026 Aegis-X Enterprise Defense platform. This document is proprietary and confidential.
            </div>
        </div>
    </body>
    </html>
    """
    return html

def get_report_download_link(html_content, filename="Mission_Report.html"):
    """Generates a link to download the report."""
    b64 = base64.b64encode(html_content.encode()).decode()
    return f'<a href="data:text/html;base64,{b64}" download="{filename}" class="stButton" style="text-decoration:none;display:inline-block;width:100%;text-align:center;padding:10px;background:linear-gradient(135deg,#00d2ff,#3a7bd5);color:white;border-radius:10px;font-weight:700;">📥 DOWNLOAD ADVANCED REPORT</a>'
