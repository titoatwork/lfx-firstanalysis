# sig-parameters archive digest (public RSS)

Total items: 20

### 1. Agenda (2026/07/17)
Date: Wed, 15 Jul 2026 11:18:32 -0700
From: adingank@... (Ajit Dingankar)
Link: https://lists.riscv.org/g/sig-parameters/message/185

Here’s the proposed agenda for the upcoming meeting this Friday, July 17 th . Opens James Ball: Presentation of work on manual parameter extraction and export to UDB Ishaan Arora and Allen Baum: Update on Gen-AI based Parameter Extraction Pipeline Discussion: M-mode parameters for RVM profile Thanks, Ajit ==== Ajit Dingankar Qualcomm Technologies, Inc. Folsom, California Book time to meet with me

---

### 2. Re: [sig-unifieddb] UDB and Parameters discussion
Date: Mon, 29 Jun 2026 14:39:06 -0700
From: @...
Link: https://lists.riscv.org/g/sig-parameters/message/184

Paul asked: > How might this fit into a "UDB data moves into ISA manual repo" scenario? The params.yaml files would be located in the ISA manual repo along with the normative rule YAML files (both per-chapter). The Python tools to parse the params.yaml files and create the params.json, params.html, or individual param YAML files for UDB already exist in the docs-resources repo (a submodule of the ISA manual repo). We just add to the ISA manual Makefile the content required to call the Python tools and create the outputs we want. All the tools run very quickly. Then the community uses the UDB YAML files as the golden parameter information. They could also use params.json (guaranteed to have the same content) if that is easier for them to consume. We'd put all the UDB YAML files (not just params) into the ISA manual release like we already do for normative rule information.

---

### 3. Re: [sig-unifieddb] UDB and Parameters discussion
Date: Mon, 29 Jun 2026 13:25:34 -0700
From: paulclar@... (Paul Clarke)
Link: https://lists.riscv.org/g/sig-parameters/message/183

Based on your response, then: 1. There are per-chapter "params.yaml" files, created by hand. 2. All of those get combined (via "make") with normative rules data into a single "params.json" file. 3. The "params.json" file is split (via a tool) into individual parameter YAML files, ostensibly for UDB. Understanding the friendlier schema might be worthy of discussion. How might this fit into a "UDB data moves into ISA manual repo" scenario? PC

---

### 4. Re: [sig-unifieddb] UDB and Parameters discussion
Date: Mon, 29 Jun 2026 12:08:18 -0700
From: @...
Link: https://lists.riscv.org/g/sig-parameters/message/182

I say put the generated files in a separate directory AND keep the existing comments warning people not to edit them. The per-chapter params.yaml files are created by hand and I've already done it for a 1 st pass of all the parameters. I designed the schema to make it friendlier to create than the UDB parameter YAML files. Besides parameters that are based on implementation-defined behaviors (the term I use for normative rules that allow choices), I've also assigned each WARL/WLRL CSR/field to one of the pre-defined types that Allen and I created (and I refined in the process of using them in params.yaml files). Note that we'll need to sync with the other AI-based activity extracting parameters to eventually create golden list from Parameters SIG. When you do a make it reads all params.yaml files, combines them, adds information from the normative rules JSON file, and then creates a nice machine-readable JSON file with all the parameter information in it. Then tools can read this JSON file to export parameter information in whatever form is desired. I have one tool that exports UDB YAML files and another tool that creates a nice HTML representation of the parameters with hyperlinks to the normative rules. Here's a slide I created for a previous Parameters SIG meeting to discuss the topic. It starts with the AsciiDoc source files from the ISA manual (now tagged with anchors for normative text). The normative text is extracted and combined with the per-chapter hand-written norm-rule.yaml files and out comes the norm-rules.json file with information about every normative rule in the ISA manual. That part is already existing for a few months and is in the ISA manual repo (the Makefile builds the norm-rules.json file). The red rectangle contains what I'm proposing we add and I've already got it working (but not in the ISA manual repo).

---

### 5. Re: UDB and Parameters discussion
Date: Mon, 29 Jun 2026 11:51:36 -0700
From: paulclar@... (Paul Clarke)
Link: https://lists.riscv.org/g/sig-parameters/message/181

> Maybe we can discuss this in tomorrow's meeting? Sure. I don't know if we'll have a full audience at the meeting, given it's sort of a holiday-ish week in US. I don't have much else for an agenda. I'm working what I'd consider a "UDB priorities" list that we could also talk about. Folks are welcome to bring their own priorities as well > I would highly recommend that we organize the YAML files so that it is 100% clear what is static and what is generated All of the generated YAML files include a WARNING that the file is auto generated. Whether that is better or worse than putting them in a separate "generated" directory is a fair question. > Each chapter in the ISA manual has a params.yaml file that lists in a nice human-readable fashion the information about each parameter in that chapter. Then I have a simple Python generator script (written by AI) that takes all the chapter params.yaml file and puts them in on single JSON file. This is exactly how I did it for the normative rules that are already in the ISA manual. > For UDB, I have a Python script that takes all the parameters in params.json and outputs individual UDB YAML files. You feed it all the chapter param.yaml files and the norm-rules.json file (since parameters reference normative rules) and out comes a directory of UDB parameter YAML files. I did this because I think it will be easier to create and maintain the list of parameters in my params.yaml format than individual UDB YAML files that have more confusing syntax (especially JSON data type). This is a little confusing. What I gleaned from above: 1. The ISA manual has per-chapter "params.yaml" files. (How are these created?) 2. All of those get combined into a single "params.json" file. (What is the purpose of this file? It is not utilized within this flow, correct?) 3. All of those per-chapter "params.yaml" files also get split into individual parameter YAML files, ostensibly for UDB. (But these apparently have confusing syntax ... something about JSON?) PC

---

### 6. UDB and Parameters discussion
Date: Mon, 29 Jun 2026 10:28:41 -0700
From: @...
Link: https://lists.riscv.org/g/sig-parameters/message/180

At the Parameter SIG meeting last week, I was sharing some ideas related to UDB and how the YAML files that make UDB are created. Maybe we can discuss this in tomorrow's meeting? The basic idea is that some of the UDB YAML files would be generated from a higher-level representation. So, you'd have a combination of static YAML files (typically written by hand) and generated UDB YAML files. I would highly recommend that we organize the YAML files so that it is 100% clear what is static and what is generated (because we don't want people editing the generated files). Note that UDB already has some simple generators to generate UDB YAML files for things like performance counter registers and PMP config registers (required because UDB doesn't currently have the concept of arrays). These generators are written in Ruby and have a template file with a ".layout" suffix such as pmpaddrN.layout . The templates use the Ruby ERB facility to customize the output UDB YAML file for each instance. The Rakefile facility is used run the generators and create the individual UDB YAML files (e.g. pmpaddr0.yaml up to pmpaddr63.yaml). What I'm not thrilled out is that the input file to the generator (the .layout template file) and the output of the generator (the 64 pmpaddr0.yaml to pmpaddr63.yaml files) are in the same directory so it isn't clear what is static and what is generated. My thinking is to formalize this idea of generators to allow more types of generators than just the simple ERB template example for pmpaddr and to put the generated files in a directory structure that makes it clear those are generated files (so don't edit them!). This came up in the Parameters SIG because I have a generator for parameters. Each chapter in the ISA manual has a params.yaml file that lists in a nice human-readable fashion the information about each parameter in that chapter. Then I have a simple Python generator script (written by AI) that takes all the chapter params.yaml file and puts them in on single JSON file. This is exactly how I did it for the normative rules that are already in the ISA manual. You can see the JSON file containing all normative rules at https://riscv.github.io/riscv-isa-manual/snapshot/norm-rules/norm-rules.json (part of the GitHub ISA manual release) and a nice HTML representation at https://riscv.github.io/riscv-isa-manual/snapshot/norm-rules/norm-rules.html . I already have the Python scripts written & tested to create a params.json file and a corresponding

---

### 7. Meeting notes (2026/06/26)
Date: Fri, 26 Jun 2026 17:41:13 -0700
From: adingank@... (Ajit Dingankar)
Link: https://lists.riscv.org/g/sig-parameters/message/179

I’ve taken a stab at capturing some highlights of today’s meeting on the Confluence space for Parameters SIG. Please let me know of any comments/suggestions. I’ll try to add more detailed notes early next week. I’ve introduced a new section for “Future Agenda” so we can pull from there in case we miss an advance email notification of the agenda for the week. Thanks, Ajit ==== Ajit Dingankar Qualcomm Technologies, Inc. (916) 605-8291 Folsom, California Book time to meet with me

---

### 8. Self-nomination for Chair or Vice Chair
Date: Fri, 19 Jun 2026 08:19:27 -0700
From: adingank@... (Ajit Dingankar)
Link: https://lists.riscv.org/g/sig-parameters/message/178

Hello Parameters SIG! I’d like to nominate myself for Chair or Vice Chair. Name: Ajit Dingankar Affiliation: Qualcomm Technologies, Inc. Biography: I'm a principal engineer at Qualcomm in the Standards and Initiatives Organization. I've been working on RISC-V enablement since I joined Qualcomm about a year ago, mainly on Unified DB modeling and associated collateral generation. I jointly drove a capstone project at Harvey Mudd College on customizing an IDE (Eclipse) for UDB files, to provide a more modern experience of software development such as content assist and cross refencing. I also jointly guided a RISC-V International Mentorship on Parameter Extraction with LLMs. Previously I worked at Intel for 27 years in various teams from x86 ISA modeling, simulation, validation, high-level synthesis and virtual platforms. Statement of Intent: I envision three main areas of work in the Parameter SIG: (1) Supporting current needs of other parts of the RISC-V community such as RVA23 certification requirements, (2) Supporting configuration requirements of tools such as UDB and Sail; and (3) Enabling new methodologies for creation and analysis of parameters for future use cases such as requiring new extensions and profiles to provide definitions of associated parameters and developing new tools that are parameterized from inception. I will organize and contribute to the work on developing a robust framework for parameter definition that will be useful for the broader community over a longer period of time, balancing the effort to deliver on present needs and to fit into the present environment. Thank you for your support! Regards, Ajit ==== Ajit Dingankar Qualcomm Technologies, Inc.

---

### 9. Reminder: Call for Candidates — Open Chair & Vice-Chair Positions (HCs, ICs, TGs, SIGs)
Date: Mon, 15 Jun 2026 05:48:37 -0700
From: rafael@... (Rafael Sene)
Link: https://lists.riscv.org/g/sig-parameters/message/177

Greetings, This is a reminder that the Call for Candidates is open for Chair and Vice-Chair positions across many RISC-V Horizontal Committees (HCs), ISA Committees (ICs), Task Groups (TGs), and Special Interest Groups (SIGs). Several positions remain open without any applicant, and we encourage qualified members to step forward. How to apply Use the nomination form: https://www.surveymonkey.com/r/riscv-call-for-candidates , select the group and the position (Chair, Vice-Chair, or Chair OR Vice-Chair) you are applying for, and provide: Your name and member affiliation A brief bio (under 500 words) A statement of intent (under 500 words) Also send your application to the group's mailing list, and please ensure you are subscribed to it. If you have any questions, or would like the current list of open positions for a specific group, please reach out to help@... . Atenciosamente | Sincerely Rafael Peria de Sene Technical Program Manager, RISC-V Phone: +55 19 98153 9778 E-mail: rafael@...

---

### 10. Re: Meeting today?
Date: Fri, 12 Jun 2026 08:23:19 -0700
From: rafael@... (Rafael Sene)
Link: https://lists.riscv.org/g/sig-parameters/message/176

Thanks, I still had it. Atenciosamente | Sincerely Rafael Peria de Sene Technical Program Manager, RISC-V Phone: +55 19 98153 9778 E-mail: rafael@... --- I sent this email when it was convenient for me. Please reply whenever it works best for you! On 12 Jun 2026 at 11:39:54, Rafael Sene via lists.riscv.org <rafael= riscv.org@... > wrote:

---

### 11. Re: Meeting today?
Date: Fri, 12 Jun 2026 08:05:34 -0700
From: adingank@... (Ajit Dingankar)
Link: https://lists.riscv.org/g/sig-parameters/message/175

The meeting was already cancelled last week. It’s not on my calendar! Thanks, Ajit ====

---

### 12. Meeting today?
Date: Fri, 12 Jun 2026 07:39:57 -0700
From: rafael@... (Rafael Sene)
Link: https://lists.riscv.org/g/sig-parameters/message/174

Are you going to meet today or should we cancel the meeting? Atenciosamente | Sincerely Rafael Peria de Sene Technical Program Manager, RISC-V Phone: +55 19 98153 9778 E-mail: rafael@... --- I sent this email when it was convenient for me. Please reply whenever it works best for you!

---

### 13. Re: M-mode CSR parameters
Date: Mon, 08 Jun 2026 15:30:34 -0700
From: david_harris@... (David Harris)
Link: https://lists.riscv.org/g/sig-parameters/message/173

Found the list,

---

### 14. Call for Candidates | 2026 Parameters SIG (Chair and Vice-Chair)
Date: Tue, 02 Jun 2026 10:04:29 -0700
From: rafael@... (Rafael Sene)
Link: https://lists.riscv.org/g/sig-parameters/message/172

Greetings, We are pleased to announce the Call for Candidates for the Parameters SIG. We invite qualified individuals to submit their candidacy for the positions of Chair and Vice-Chair. Candidate Submission Details Candidates must submit a biography (bio) and statement of intent by June 16, 2026. The current charter / Proposal of Work for the Parameters SIG can be found here: https://riscv.atlassian.net/wiki/spaces/PRMT/pages/812023811/Parameter+SIG+PoW The Jira for this Technical Committee is: https://riscv.atlassian.net/browse/RVC-928 Important: please ensure you are subscribed to this Technical Committee mailing list at https://lists.riscv.org/g/sig-parameters Nomination Process If you would like to nominate yourself, please use this form [1], where you will provide: - Candidate's name and member affiliation; - Brief bio (under 500 words); - Statement of intent (under 500 words). Important: You must also send your application to the Parameters SIG mailing list at https://lists.riscv.org/g/sig-parameters . You can follow the applications by clicking here (you must be part of the RISC-V Team at GitHub to see this). Qualifications We are looking for candidates with expertise in RISC-V ISA parameterization and configuration modeling, familiarity with the UnifiedDB and profiles work, and experience translating implementation options into a coherent, machine-readable parameter framework. Responsibilities - Collaborating with existing Technical Committees. - Facilitating contributions aligned with the Technical Committee charter. - Publishing meeting minutes and reports. - Contributing to the RISC-V Tech Journal. - Serving as an editor/reviewer for certain proposals. - Engaging with the community via Meetings, Confluence, Jira, Mailing Lists, and GitHub. - Responding to queries within 48 hours. - Managing and running regular meetings when applicable. - Attending Technical Operations Meetings (and occasional Technical Operations Overflow Meeting). If you have any questions or require more information, please don't hesitate to reach out to help@... . We appreciate your participation and look forward to receiving your nominations! [1] - https://www.surveymonkey.com/r/riscv-call-for-candidates Atenciosamente | Sincerely Rafael Peria de Sene Technical Program Manager, RISC-V Phone: +55 19 98153 9778 E-mail: rafael@... --- I sent this email when it was convenient for me. Please reply whenever it works best for you!

---

### 15. Re: Voting status
Date: Sat, 23 May 2026 00:06:28 -0700
From: allenbaum.riscv@... (Allen Baum)
Link: https://lists.riscv.org/g/sig-parameters/message/171

I added myself as voting, assuming I can. I have been attending meetings.

---

### 16. Parameter Extraction Mentorship status report
Date: Fri, 22 May 2026 10:42:17 -0700
From: adingank@... (Ajit Dingankar)
Link: https://lists.riscv.org/g/sig-parameters/message/170

I’ve attached the RVI Spring 2026 mentorship status report prepared by Ishaan Arora for your reference, as I had mentioned in the Parmeter SIG meeting today. It described the progress as of last week, and contains the Issue and corresponding PR numbers for all 8 phases of the mentorship. Please let me know if you have any questions or comments. Thanks, Ajit ==== Ajit Dingankar Qualcomm Technologies, Inc. (916) 605-8291 Folsom, California Book time to meet with me

---

### 17. Voting status
Date: Fri, 22 May 2026 09:50:59 -0700
From: derek.hower.os@... (Derek Hower)
Link: https://lists.riscv.org/g/sig-parameters/message/169

As we move to start elections for Chair and Vice Chair of the Parameters SIG, please visit the following to update voting status. Participation and Voting Rights - Parameters SIG - RISC-V Tech Hub As of right now, we only have three declared voters, which I do not believe is enough to make quorum. Thanks, -Derek Book time to meet with me

---

### 18. Meeting Cancelled
Date: Fri, 15 May 2026 08:09:17 -0700
From: derek.hower.os@... (Derek Hower)
Link: https://lists.riscv.org/g/sig-parameters/message/168

Ajit was going to present the work that him and mentees have been doing on parameter extraction, but he has come down sick. We'll move that presentation to next week. -Derek Book time to meet with me

---

### 19. Re: Is today’s meetings really cancelled?
Date: Fri, 08 May 2026 09:02:14 -0700
From: derek.hower.os@... (Derek Hower)
Link: https://lists.riscv.org/g/sig-parameters/message/167

Yes, still working on the list in UDB. Book time to meet with me

---

### 20. Is today’s meetings really cancelled?
Date: Fri, 08 May 2026 08:57:17 -0700
From: rafael@... (Rafael Sene)
Link: https://lists.riscv.org/g/sig-parameters/message/166

Is today’s meetings really cancelled? Atenciosamente | Sincerely Rafael Peria de Sene Technical Program Manager, RISC-V Phone: +55 19 98153 9778 E-mail: rafael@... --- I sent this email when it was convenient for me. Please reply whenever it works best for you!

---
