<?php

// Add double quotes if the field contains a comma
function addDoubleQuoteIfComma($CSVstring) {
    if (strpos($CSVstring, ',') !== false) {
        $newCSVstring = '"' . $CSVstring . '"';
    } else {
        $newCSVstring = $CSVstring;
    }
    return $newCSVstring;
}

// work with get or post
$request = array_merge($_GET, $_POST);

$outputfilename = $request['filename'];

$decoded_response = json_decode(file_get_contents('php://input'), true);

//New code with dynamic output file
// Check if file already exists
if (file_exists($outputfilename)) {
	//Open file
	$fp = fopen($outputfilename,'a');
} else {
	//Create file
	$fp = fopen($outputfilename,'a');
	//Add header
	// Full response
	//fwrite($fp,"status,status_message,lookup_outcome,lookup_outcome_message,request_id,international_format_number,country_code,country_code_iso3,country_name,country_prefix,request_price,remaining_balance,current_carrier | network_code,current_carrier | name,current_carrier | country,current_carrier | network_type,original_carrier | network_code,original_carrier | name,original_carrier | country,original_carrier | network_type,valid_number,reachable,ported,roaming | status,ip_warnings\n");
    // Hide request_price and remaining_balance
    fwrite($fp,"status,status_message,lookup_outcome,lookup_outcome_message,request_id,international_format_number,country_code,country_code_iso3,country_name,country_prefix,current_carrier | network_code,current_carrier | name,current_carrier | country,current_carrier | network_type,original_carrier | network_code,original_carrier | name,original_carrier | country,original_carrier | network_type,valid_number,reachable,ported,roaming | status,ip_warnings,caller_name,first_name,last_name,caller_type\n");
}

if ($decoded_response['status'] == 0) {
    // Full response
	//fwrite($fp,"{$decoded_response['status']},{$decoded_response['status_message']},{$decoded_response['lookup_outcome']},{$decoded_response['lookup_outcome_message']},{$decoded_response['request_id']},{$decoded_response['international_format_number']},{$decoded_response['country_code']},{$decoded_response['country_code_iso3']},{$decoded_response['country_name']},{$decoded_response['country_prefix']},{$decoded_response['request_price']},{$decoded_response['remaining_balance']},{$decoded_response['current_carrier']['network_code']},{$decoded_response['current_carrier']['name']},{$decoded_response['current_carrier']['country']},{$decoded_response['current_carrier']['network_type']},{$decoded_response['original_carrier']['network_code']},{$decoded_response['original_carrier']['name']},{$decoded_response['original_carrier']['country']},{$decoded_response['original_carrier']['network_type']},{$decoded_response['valid_number']},{$decoded_response['reachable']},{$decoded_response['ported']},{$decoded_response['roaming']['status']},{$decoded_response['ip_warnings']}\n");
	// Hide request_price and remaining_balance
	$currentCarrierName = addDoubleQuoteIfComma($decoded_response['current_carrier']['name']);
	$originalCarrierName = addDoubleQuoteIfComma($decoded_response['original_carrier']['name']);
	if ($decoded_response['caller_name'] == 'unknown') {
	    fwrite($fp,"{$decoded_response['status']},{$decoded_response['status_message']},{$decoded_response['lookup_outcome']},{$decoded_response['lookup_outcome_message']},{$decoded_response['request_id']},{$decoded_response['international_format_number']},{$decoded_response['country_code']},{$decoded_response['country_code_iso3']},{$decoded_response['country_name']},{$decoded_response['country_prefix']},{$decoded_response['current_carrier']['network_code']},{$currentCarrierName},{$decoded_response['current_carrier']['country']},{$decoded_response['current_carrier']['network_type']},{$decoded_response['original_carrier']['network_code']},{$originalCarrierName},{$decoded_response['original_carrier']['country']},{$decoded_response['original_carrier']['network_type']},{$decoded_response['valid_number']},{$decoded_response['reachable']},{$decoded_response['ported']},{$decoded_response['roaming']['status']},{$decoded_response['ip_warnings']},{$decoded_respons['caller_name']},,,{$decoded_response['caller_type']}\n");
    } else {
        fwrite($fp,"{$decoded_response['status']},{$decoded_response['status_message']},{$decoded_response['lookup_outcome']},{$decoded_response['lookup_outcome_message']},{$decoded_response['request_id']},{$decoded_response['international_format_number']},{$decoded_response['country_code']},{$decoded_response['country_code_iso3']},{$decoded_response['country_name']},{$decoded_response['country_prefix']},{$decoded_response['current_carrier']['network_code']},{$currentCarrierName},{$decoded_response['current_carrier']['country']},{$decoded_response['current_carrier']['network_type']},{$decoded_response['original_carrier']['network_code']},{$originalCarrierName},{$decoded_response['original_carrier']['country']},{$decoded_response['original_carrier']['network_type']},{$decoded_response['valid_number']},{$decoded_response['reachable']},{$decoded_response['ported']},{$decoded_response['roaming']['status']},{$decoded_response['ip_warnings']},{$decoded_response['caller_name']},{$decoded_response['first_name']},{$decoded_response['last_name']},{$decoded_response['caller_type']}\n");
    }
} else {
    fwrite($fp,"Error,{$decoded_response['status']},{$decoded_response['error_text']},,,,,,,,,,,,,,,,,,,,,,,,\n");
}


//Old code - non dynamic output file
/*
// Check if file already exists
if (file_exists('ni_async_cb.txt')) {
	//Open file
	$fp = fopen('ni_async_cb.txt','a');
} else {
	//Create file
	$fp = fopen('ni_async_cb.txt','a');
	//Add header
	fwrite($fp,"status,status_message,lookup_outcome,lookup_outcome_message,request_id,international_format_number,country_code,country_code_iso3,country_name,country_prefix,request_price,remaining_balance,current_carrier | network_code,current_carrier | name,current_carrier | country,current_carrier | network_type,original_carrier | network_code,original_carrier | name,original_carrier | country,original_carrier | network_type,valid_number,reachable,ported,roaming | status,ip_warnings\n");
}

if ($decoded_response['status'] == 0) {
	fwrite($fp,"{$decoded_response['status']},{$decoded_response['status_message']},{$decoded_response['lookup_outcome']},{$decoded_response['lookup_outcome_message']},{$decoded_response['request_id']},{$decoded_response['international_format_number']},{$decoded_response['country_code']},{$decoded_response['country_code_iso3']},{$decoded_response['country_name']},{$decoded_response['country_prefix']},{$decoded_response['request_price']},{$decoded_response['remaining_balance']},{$decoded_response['current_carrier']['network_code']},{$decoded_response['current_carrier']['name']},{$decoded_response['current_carrier']['country']},{$decoded_response['current_carrier']['network_type']},{$decoded_response['original_carrier']['network_code']},{$decoded_response['original_carrier']['name']},{$decoded_response['original_carrier']['country']},{$decoded_response['original_carrier']['network_type']},{$decoded_response['valid_number']},{$decoded_response['reachable']},{$decoded_response['ported']},{$decoded_response['roaming']['status']},{$decoded_response['ip_warnings']}\n");
} else {
    fwrite($fp,"Error,{$decoded_response['status']},{$decoded_response['error_text']},,,,,,,,,,,,,,,,,,,,,,,,\n");
}
*/

header("Status: 200");

fclose($fp);
?>