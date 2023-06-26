$(document).ready(function() {
  // Handle form submission
  $('#expenseForm').on('submit', function(e) {
    e.preventDefault();

    // Get form values
    var date = $('#dateInput').val();
    var amount = $('#amountInput').val();
    var category = $('#categoryInput').val();
    var notes = $('#notesInput').val();

    // Create expense object
    var expense = {
      date: date,
      amount: amount,
      category: category,
      notes: notes
    };

    // Make API request to create expense
    $.ajax({
      url: '/api/expenses/',
      type: 'POST',
      data: JSON.stringify(expense),
      contentType: 'application/json',
      success: function(response) {
        // Clear form fields
        $('#dateInput').val('');
        $('#amountInput').val('');
        $('#categoryInput').val('');
        $('#notesInput').val('');

        // Refresh expenses list
        getExpenses();
      }
    });
  });
