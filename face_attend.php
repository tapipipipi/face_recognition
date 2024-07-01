<?php
/**
* File : exchange.php
* Date : 2024/06/25
* Author : H.Kitagawa
*/

// Pythonからデータ受け取り
if(isset($_POST['testdata'])){
    $faceData = $_POST['testdata'];
    $faceData = json_decode($faceData, true);   //数値に変換
    
}