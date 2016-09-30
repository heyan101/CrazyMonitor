# coding:utf8
import json

from docx import Document
from docx.shared import Pt


class Docparse(object):

    def __init__(self):
        self.data = """
            {"127.0.0.1":{"Service": {"Ufa": {"unode": "started", "CENTER_NODE_ADDR": "http://127.0.0.1:9090/uctr/stor",
            "uctr": "started"}, "Xserver": {"xserver.mysql.host": "jdbc:mysql://127.0.0.1","server": "started"},"Mysql":
            {"server": "started"}}, "Server": {"MEM": {"swap_used": "0B", "swap_free": "2.0G", "mem_buffers": "106.7M",
            "mem_used": "1.2G", "mem_total": "1.8G", "mem_used_rate": "65.17", "mem_free_rate": "34.83", "mem_cached":
            "505.7M", "swap_total": "2.0G", "mem_free": "652.6M", "swap_used_rate": "0.00", "swap_free_rate": "100.00"},
            "DISK": [{"used": "6.4G", "free": "10.9G", "fstype": "ext4", "dev": "/dev/mapper/VolGroup-lv_root", "path":
            "/", "total": "17.3G", "used_rate": "37.11"}, {"used": "38.7M", "free": "445.5M", "fstype": "ext4",
            "dev": "/dev/sda1", "path": "/boot", "total": "484.2M", "used_rate": "8.00"}], "CPU": {"cores":
            [{"model": "Intel(R) Core(TM) i7-6700HQ CPU @ 2.60GHz", "bits": "64bit"}], "cpu_count": 1, "core_count"
            : 1}}}}
        """

    def parse(self):
        data = json.loads(self.data)

        document = Document()

        # title
        document.add_heading(u'巡检日志', 0)
        document.add_paragraph(u'Service IP：' + '127.0.0.1', style='Normal')

        document.add_heading(u'Ufa', 1)
        # table
        table = document.add_table(rows=1, cols=3, style='Table Grid')
        table.autofit = False
        tb_cells = table.rows[0].cells
        tb_cells[0].text = 'unode'
        tb_cells[1].text = 'CENTER_NODE_ADDR'
        tb_cells[2].text = 'uctr'

        row_cells = table.add_row().cells
        row_cells[0].text = 'started'
        row_cells[1].text = 'http://127.0.0.1:9090/uctr/stor'
        row_cells[2].text = 'started'

        document.add_heading(u'Xserver', 1)
        table = document.add_table(rows=1, cols=2, style='Table Grid')
        table.autofit = False
        tb_cells = table.rows[0].cells
        tb_cells[0].text = 'xserver.mysql.host'
        tb_cells[1].text = 'server'

        row_cells = table.add_row().cells
        row_cells[0].text = 'jdbc:mysql://127.0.0.1'
        row_cells[1].text = 'started'

        document.save(u'巡检日志.docx')


if __name__ == "__main__":
    doc = Docparse()
    doc.parse()
