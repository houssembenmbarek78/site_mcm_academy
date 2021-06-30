  window.intercomSettings = {
    app_id: "pe98h7lm",
    name: "{{ request.user.name|escapejs }}", // Full name
    email: "{{ request.user.email|escapejs }}", // Email address
    created_at: "{{ request.user.date_joined|date:"U" }}" // Signup date as a Unix timestamp
  };
