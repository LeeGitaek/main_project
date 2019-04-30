var files = e.target.files || e.dataTransfer.files;
var a = $('input#fileselect.addFile');
a[a.length-1].files = file;
// getElementById
function $id(id) {
 return document.getElementById(id);
}
// output information
function Output(msg) {
 var m = $id("list");
 m.innerHTML = msg + m.innerHTML;
}
// call initialization file
if (window.File && window.FileList && window.FileReader) {
 Init();
}
// initialize
function Init() {
 var fileselect = $id("fileselect"),
   filedrag = $id("filedrag"),
   submitbutton = $id("submitbutton");
 // file select
 fileselect.addEventListener("change", FileSelectHandler, false);
 // is XHR2 available?
 var xhr = new XMLHttpRequest();
 if (xhr.upload) {
   // file drop
   filedrag.addEventListener("dragover", FileDragHover, false);
   // filedrag.addEventListener("dragleave", FileDragHover, false);
   filedrag.addEventListener("drop", FileSelectHandler, false);
   filedrag.style.display = "block";
   // remove submit button
   submitbutton.style.display = "none";
 }
}
// file drag hover
function FileDragHover(e) {
 e.stopPropagation();
 e.preventDefault();
 e.target.className = (e.type == "dragover" ? "hover" : "");
}
// file selection
function FileSelectHandler(e) {
 // cancel event and hover styling
   FileDragHover(e);
 // fetch FileList object
 var files = e.target.files || e.dataTransfer.files;
   console.log('te');
   addFileFromLastInput(files);
   // process all File objects
 for (var i = 0, f; f = files[i]; i++) {
   ParseFile(f);
 }
}
function ParseFile(file) {
   var fileName = file.name,
       fileType = file.type,
       fileSize = file.size + 'bytes';
 Output(
   "<tr><td>" + fileName +
   "</td><td>" + fileType +
   "</td><td>" + fileSize +
   "</td> </tr>"
 );
}
function addFileFromLastInput(file){
   var a = $('input#fileselect.addFile');
   a[a.length-1].files = file;
   try{
       let new_input = '<input id="fileselect" type="file" name="fileselect" multiple="multiple" class="addFile" />';
       $('.files').append(new_input);
   }catch(err){
   }
   return 0;
}
