window.intercomSettings = {
  app_id: "pe98h7lm",
  name: "<%= current_user.name %>", // Full name
  email: "<%= current_user.email %>", // Email address
  created_at: "<%= current_user.created_at.to_i %>", // Signup date as a Unix timestamp
};
