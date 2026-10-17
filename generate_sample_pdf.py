"""
generate_sample_pdf.py - Generates an authentic sample NPTEL lecture notes PDF
for instant testing in the application.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_sample_nptel_pdf(output_path="sample_nptel_lecture.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F2942'),
        alignment=1, # Center
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=14,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        leftIndent=15,
        spaceAfter=4
    )
    
    story = []
    
    # Header
    story.append(Paragraph("NPTEL Online Certification Course", title_style))
    story.append(Paragraph("Course: Cloud Computing & Distributed Systems | Week 3: Virtualization & Hypervisors", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))
    
    # Section 1
    story.append(Paragraph("1. Introduction to Virtualization in Cloud Computing", h1_style))
    story.append(Paragraph(
        "Virtualization is the fundamental foundational technology that enables cloud computing. It allows multiple operating systems "
        "and applications to run concurrently on a single physical host by abstracting the underlying physical hardware resources. "
        "Through virtualization, cloud service providers achieve high resource utilization, multi-tenancy, and rapid elasticity.",
        body_style
    ))
    story.append(Paragraph("Essential goals of virtualization in cloud infrastructure include:", body_style))
    story.append(Paragraph("• <b>Resource Pooling:</b> Aggregating compute, memory, and storage across homogeneous or heterogeneous servers.", bullet_style))
    story.append(Paragraph("• <b>Isolation & Security:</b> Ensuring guest virtual machines cannot access or compromise each other's memory space.", bullet_style))
    story.append(Paragraph("• <b>Workload Migration:</b> Enabling live migration of running VMs between physical hosts with minimal downtime.", bullet_style))
    story.append(Paragraph("• <b>High Availability & Disaster Recovery:</b> Rapid checkpointing and snapshot restoration.", bullet_style))
    
    story.append(Spacer(1, 10))
    
    # Section 2
    story.append(Paragraph("2. Hypervisor Taxonomy: Type-1 vs Type-2", h1_style))
    story.append(Paragraph(
        "A Hypervisor, also termed a Virtual Machine Monitor (VMM), is the software layer that controls hardware access for guest VMs. "
        "Hypervisors are strictly classified into two primary architectural types:",
        body_style
    ))
    
    table_data = [
        ["Attribute", "Type-1 Hypervisor (Bare-Metal)", "Type-2 Hypervisor (Hosted)"],
        ["Underlying Layer", "Directly on Physical Hardware", "Runs on top of a Host Operating System"],
        ["Performance", "Near-native performance, low latency", "Lower performance due to OS context switches"],
        ["Resource Overhead", "Minimal microkernel footprint", "Significant footprint of host OS + hypervisor"],
        ["Typical Use Cases", "Enterprise Datacenters, AWS EC2, Azure", "Software testing, Local development"],
        ["Popular Examples", "VMware ESXi, Xen, KVM, MS Hyper-V", "Oracle VirtualBox, VMware Workstation"]
    ]
    
    t = Table(table_data, colWidths=[110, 210, 210])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    
    story.append(Spacer(1, 15))
    
    # Section 3
    story.append(Paragraph("3. Full Virtualization vs Paravirtualization", h1_style))
    story.append(Paragraph(
        "In classical x86 architecture, 17 sensitive instructions could not be virtualized without special intervention. "
        "Two prominent software techniques evolved to solve this:",
        body_style
    ))
    story.append(Paragraph("• <b>Full Virtualization (Binary Translation):</b> Guest OS is completely unmodified. Sensitive privileged instructions are dynamically rewritten at runtime into safe hypervisor instructions. Examples include early VMware ESX.", bullet_style))
    story.append(Paragraph("• <b>Paravirtualization (Hypercalls):</b> The guest OS kernel is modified to recognize it is running in a virtualized container. Instead of executing sensitive instructions, it makes direct software traps called <i>Hypercalls</i> to the VMM (pioneered by Xen).", bullet_style))
    story.append(Paragraph("• <b>Hardware-Assisted Virtualization:</b> Intel VT-x and AMD-V added root/non-root CPU modes (Ring -1), allowing unmodified guest OS to run at native speeds with hardware-enforced traps.", bullet_style))
    
    story.append(Spacer(1, 10))
    
    # Section 4
    story.append(Paragraph("4. Service Level Agreements (SLA) & Reliability Calculations", h1_style))
    story.append(Paragraph(
        "In commercial cloud deployments, availability is governed by legal Service Level Agreements (SLAs). "
        "System availability $A$ is formulated mathematically as:",
        body_style
    ))
    story.append(Paragraph("<b>Availability Formula:</b> A = MTTF / (MTTF + MTTR) * 100%", ParagraphStyle('Formula', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F766E'), leftIndent=20)))
    story.append(Paragraph("Where <b>MTTF</b> is Mean Time To Failure, and <b>MTTR</b> is Mean Time To Repair.", body_style))
    story.append(Paragraph("• Five Nines (99.999%): Maximum allowed downtime of ~5.26 minutes per year.", bullet_style))
    story.append(Paragraph("• Four Nines (99.99%): Maximum allowed downtime of ~52.6 minutes per year.", bullet_style))
    story.append(Paragraph("• Three Nines (99.9%): Maximum allowed downtime of ~8.76 hours per year.", bullet_style))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("5. NPTEL Assignment Review & Key Questions", h1_style))
    story.append(Paragraph("Be prepared to calculate serial and parallel availability and distinguish between elasticity (autonomic workload adaptation) and scalability (structural capacity expansion).", body_style))
    
    doc.build(story)
    print(f"Generated sample NPTEL PDF successfully at: {output_path}")

if __name__ == "__main__":
    create_sample_nptel_pdf()
