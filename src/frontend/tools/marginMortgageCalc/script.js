google.charts.load('44', {
  callback: calc,
  packages: ['corechart']
});

function calc() {
// Givens
  var houseValue = parseFloat(document.getElementById("houseValue").value);
  var homeExpectedReturn = parseFloat(document.getElementById("homeExpectedReturn").value);
  var downpaymentPercent = parseFloat(document.getElementById("downpaymentPercent").value);
  var mortgageInterest = parseFloat(document.getElementById("mortgageInterest").value);
  var stockValue = parseFloat(document.getElementById("stockValue").value);
  var stockExpectedReturn = parseFloat(document.getElementById("stockExpectedReturn").value);
  var rentCost = parseFloat(document.getElementById("rentCost").value);
  var marginInterest = parseFloat(document.getElementById("marginInterest").value);
  var loanTerm = parseFloat(document.getElementById("loanTerm").value);

// Imputed
  var loanPrincipal = houseValue * (1.0 - downpaymentPercent);
  var monthlyMortgageInterestRate = mortgageInterest / 12.0;
  var loanTermMonths = loanTerm * 12.0;
  var monthlyMortgagePayment = (monthlyMortgageInterestRate * loanPrincipal)/(1.0 - (1.0 + monthlyMortgageInterestRate)**(-1.0 * loanTermMonths));
  var annualMortgageCost = monthlyMortgagePayment * 12.0;
  var marginPercentage = houseValue * downpaymentPercent / stockValue;
  var marginValue = stockValue * marginPercentage;
  var annualMarginInterestPayment = marginInterest * marginValue;
  var expectedEquityReturnNominal = stockExpectedReturn * stockValue;
  var expectedHomeAppreciationNominal = homeExpectedReturn * houseValue;

// Buy the home with margin
  var totalAnnualHomeOwningCost = annualMortgageCost + annualMarginInterestPayment;
  var totalAnnualHomeOwningReturn = expectedEquityReturnNominal + expectedHomeAppreciationNominal;
  var netHomeOwningReturn = totalAnnualHomeOwningReturn - totalAnnualHomeOwningCost;
  var netHomeOwningReturnRate = netHomeOwningReturn / stockValue;

// Rent and own stocks
  var totalAnnualNonHomeCost = rentCost * 12.0;
  var netReturnNonHome = expectedEquityReturnNominal - totalAnnualNonHomeCost;
  var netReturnNonHomeRate = netReturnNonHome / expectedEquityReturnNominal;

// Returns
  var thirtyYearRentingStock = [stockValue * (1.0 + stockExpectedReturn) - totalAnnualNonHomeCost];
  var thirtyYearHouseStock = [stockValue * (1.0 + stockExpectedReturn) - totalAnnualHomeOwningCost];
  var thirtyYearHouseProperty = [houseValue * (1.0 + homeExpectedReturn)];
  var mortgageBalanceRemaining = [(monthlyMortgagePayment / monthlyMortgageInterestRate) * (1.0 - (1.0 / (1.0 + monthlyMortgageInterestRate)**(loanTermMonths - 12)))];
  var thirtyYearHouseTotal = [thirtyYearHouseStock[0] + thirtyYearHouseProperty[0] - mortgageBalanceRemaining[0] - marginValue];

// No margin Returns
  var thirtyYearNoMarginStock = [(stockValue - marginValue) * (1.0 + stockExpectedReturn) - annualMortgageCost];
  var thirtyYearNoMarginTotal = [thirtyYearNoMarginStock[0] + thirtyYearHouseProperty[0] - mortgageBalanceRemaining[0]];

  for (var i = 1; i < loanTerm; ++i) {
    thirtyYearRentingStock.push(thirtyYearRentingStock[i-1] * (1.0 + stockExpectedReturn) - totalAnnualNonHomeCost);
    thirtyYearHouseStock.push(thirtyYearHouseStock[i-1] * (1.0 + stockExpectedReturn) - totalAnnualHomeOwningCost);
    thirtyYearHouseProperty.push(thirtyYearHouseProperty[i-1] * (1.0 + homeExpectedReturn));
    mortgageBalanceRemaining.push((monthlyMortgagePayment / monthlyMortgageInterestRate) * (1.0 - (1.0 / (1.0 + monthlyMortgageInterestRate)**(loanTermMonths - (12 * (i + 1))))));
    thirtyYearHouseTotal.push(thirtyYearHouseStock[i] + thirtyYearHouseProperty[i] - mortgageBalanceRemaining[i] - marginValue);
    thirtyYearNoMarginStock.push(thirtyYearNoMarginStock[i-1] * (1.0 + stockExpectedReturn) - annualMortgageCost);
    thirtyYearNoMarginTotal.push(thirtyYearNoMarginStock[i] + thirtyYearHouseProperty[i] - mortgageBalanceRemaining[i]);
  }

  var dataInput = [];
  for (var i = 1; i <= loanTerm; ++i) {
    var curr = [];
    curr.push(i);
    curr.push(thirtyYearRentingStock[i-1]);
    curr.push(thirtyYearHouseTotal[i-1]);
    curr.push(thirtyYearNoMarginTotal[i-1]);
    curr.push(mortgageBalanceRemaining[i-1]);
    dataInput.push(curr);
  }

  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Year');
  data.addColumn('number', 'Renting Value');
  data.addColumn('number', 'Net Owning w/ Margin Value');
  data.addColumn('number', 'Net Owning w/o Margin Value');
  data.addColumn('number', 'Mortgage Balance');

  data.addRows(dataInput);

  var options = {
    hAxis: {
      title: 'Year'
    },
    vAxis: {
      title: 'Value'
    },
    backgroundColor: '#f1f8e9'
  };

  var chart = new google.visualization.LineChart(document.getElementById('ReturnsGraph'));
  chart.draw(data, options);
}