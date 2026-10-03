#target indesign

// Worker: open template, import the XML named in the job file, map styles, save, close.
// Job path is the first argument after the script path when launched from the orchestrator.
// Safe to re-run: it overwrites the output .indd named in the job.

(function () {
    var jobPath = $.getenv("MACRO_JOB") || "";
    if (!jobPath && arguments && arguments.length) {
        jobPath = String(arguments[0]);
    }
    if (!jobPath || !File(jobPath).exists) {
        $.writeln("MACRO_LAYOUTS missing job file");
        return;
    }

    var jobFile = File(jobPath);
    jobFile.open("r");
    var job = eval("(" + jobFile.read() + ")");
    jobFile.close();

    var template = File(job.template);
    if (!template.exists) {
        $.writeln("template missing: " + job.template);
        return;
    }

    var doc = app.open(template);
    try {
        var xmlFile = File(job.xml);
        if (!xmlFile.exists) {
            throw new Error("xml missing: " + job.xml);
        }
        doc.importXML(xmlFile);
        var map = job.style_map || {};
        for (var tagName in map) {
            if (!map.hasOwnProperty(tagName)) continue;
            var styleName = map[tagName];
            var style = doc.paragraphStyles.itemByName(styleName);
            var tag = doc.xmlTags.itemByName(tagName);
            if (style.isValid && tag.isValid) {
                doc.xmlImportMaps.add(tag, style);
            }
        }
        doc.mapXMLTagsToStyles();
        var out = new File(job.output);
        doc.save(out);
        $.writeln("saved " + job.output);
    } catch (err) {
        $.writeln("worker failed: " + err);
    } finally {
        doc.close(SaveOptions.NO);
    }
})();
