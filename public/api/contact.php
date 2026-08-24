<?php
declare(strict_types=1);
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { http_response_code(405); exit; }
if (!empty($_POST['website'] ?? '')) { header('Location: /thank-you/'); exit; }
$name=trim((string)($_POST['name']??''));$email=filter_var($_POST['email']??'',FILTER_VALIDATE_EMAIL);$message=trim((string)($_POST['message']??''));$consent=$_POST['consent']??'';
if ($name===''||!$email||$message===''||$consent!=='yes') { http_response_code(422); echo 'Please complete all required fields.'; exit; }
$to=getenv('CONTACT_TO') ?: 'hello@alankyeong.com';
$subject='Professional enquiry from '.$name;
$body="Name: $name\nEmail: $email\nOrganisation: ".trim((string)($_POST['organisation']??''))."\nInterest: ".trim((string)($_POST['interest']??''))."\nMarket: ".trim((string)($_POST['market']??''))."\n\nMessage:\n$message";
$headers=['From: alankyeong.com <no-reply@alankyeong.com>','Reply-To: '.$email,'Content-Type: text/plain; charset=UTF-8'];
if (!mail($to,$subject,$body,implode("\r\n",$headers))) { http_response_code(500); echo 'The enquiry could not be sent. Please try again later.'; exit; }
header('Location: /thank-you/',true,303);
