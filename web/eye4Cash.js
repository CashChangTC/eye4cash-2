/* show some description for this project */
function showDescription(){
	Materialize.toast('Support USD coins include of 1 cent, 10 cent and 25 cent. ', 4000)
}
/* mapping classNo to class name */
function classNo2Name(classNo){
	if(classNo==0)
		return "1 cent";
	if(classNo==1)
		return "10 cent";
	if(classNo==2)
		return "25 cent";
}
/* to do predicit*/
function uploadPrediction() {
	var queryData = {
		photoURL: $("#form_fileURL").val()
	};
	$("#btnStart").hide();
	$("#answerString").text("");
	$("#loadingIcon").show();
	var delayMillis = 1000; //1 second
	setTimeout(function () {
		$.ajax({
			method: "POST",
			async: false,
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			url: "service.restful.php",
			data: JSON.stringify(queryData),
			statusCode: {
				200: function (respone) {
					$("#fileSelectInput").show();
					$("#btnStart").hide();
					$("#loadingIcon").hide();
					if(respone["result"]){
						name = classNo2Name(respone["class"]);
						Materialize.toast("Answer = "+name, 4000,'rounded');
						$("#answerString").html("<i class=\"small material-icons\">chevron_right</i> I think ... it a "+name+" right?");
					}else{
						Materialize.toast("Detect fail :(", 4000,'rounded');
						$("#answerString").html("<i class=\"small material-icons\">chevron_right</i> Detect fail :(");
					
					}
				},
				404: function (respone) {
					alert("not found");
					console.log(respone);
				},
				406: function (respone) {
					alert("loss index");
					console.log(respone);
				},
				500: function (respone) {
					alert("server error");
					console.log(respone);
				}
			}
		});
	}, delayMillis);
}