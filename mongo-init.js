db.words.createIndex({ "label": 1 }, { unique: true });

var text = cat("/tmp/db.json");

jsObj = JSON.parse(text);

jsObj.map(i => db.words.insert({label: i.label, russian: i.russian}))