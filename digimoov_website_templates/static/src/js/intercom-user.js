var user_name=document.getElementById("intercom_user_name_connected").value;
var user_email=document.getElementById("intercom_user_email_connected").value;
window.intercomSettings = {
    app_id: "pe98h7lm",
    name: user_name, // Full name
    email: user_email, // Email address
    created_at: "<%= current_user.created_at.to_i %>" // Signup date as a Unix timestamp
};
