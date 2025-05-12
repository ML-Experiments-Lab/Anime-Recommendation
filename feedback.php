<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get form data
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $message = htmlspecialchars($_POST['message']);

    // Store feedback (For simplicity, we'll store it in a file)
    $feedbackData = "Name: $name\nEmail: $email\nMessage: $message\n\n";

    // Open the feedback.txt file and append new feedback
    $file = fopen("feedback.txt", "a");
    fwrite($file, $feedbackData);
    fclose($file);

    // Send a success response to AJAX
    echo "Thank you for your feedback!";
}
?>
