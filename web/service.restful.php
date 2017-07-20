<?php
header('Content-type: application/json');
$postData = file_get_contents('php://input');
if (empty($postData))
{
    http_response_code(406);
    die("[{\"Result\":\"parameter loss\"}]");
}else{
	$DataofJson=json_decode($postData);

	$data = array(
			"photoURL" => $DataofJson->photoURL
	);
	$url = "http://goofy.server.medhub.ai:9455/v1/singlePhotoPrediction";
    $data_string = json_encode($data);
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);
    curl_setopt($ch, CURLOPT_TIMEOUT, 300);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
            'Content-Type: application/json',
            'Content-Length: ' . strlen($data_string))
    );

    $resResult = curl_exec($ch);
	echo $resResult;
}
?>