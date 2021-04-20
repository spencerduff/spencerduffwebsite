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
  var shouldInflateRent = document.getElementById("rentInflation").checked;

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
  var nYearRentingStock = [stockValue * (1.0 + stockExpectedReturn) - totalAnnualNonHomeCost];
  var nYearHouseStock = [stockValue * (1.0 + stockExpectedReturn) - totalAnnualHomeOwningCost];
  var nYearHouseProperty = [houseValue * (1.0 + homeExpectedReturn)];
  var mortgageBalanceRemaining = [(monthlyMortgagePayment / monthlyMortgageInterestRate) * (1.0 - (1.0 / (1.0 + monthlyMortgageInterestRate)**(loanTermMonths - 12)))];
  var nYearHouseTotal = [nYearHouseStock[0] + nYearHouseProperty[0] - mortgageBalanceRemaining[0] - marginValue];

// No margin Returns
  var nYearNoMarginStock = [(stockValue - marginValue) * (1.0 + stockExpectedReturn) - annualMortgageCost];
  var nYearNoMarginTotal = [nYearNoMarginStock[0] + nYearHouseProperty[0] - mortgageBalanceRemaining[0]];

// Renting out the house
  var nYearCumulativeRentReturns = [totalAnnualNonHomeCost];
// With Margin
  var nYearLandlordMarginStock = [stockValue * (1.0 + stockExpectedReturn) - totalAnnualHomeOwningCost + totalAnnualNonHomeCost];
  var nYearLandlordMarginTotal = [nYearLandlordMarginStock[0] + nYearHouseProperty[0] - mortgageBalanceRemaining[0] - marginValue];

// Without Margin
  var nYearLandlordWithoutMarginStock = [(stockValue - marginValue) * (1.0 + stockExpectedReturn) - annualMortgageCost + totalAnnualNonHomeCost];
  var nYearLandlordWithoutMarginTotal = [nYearLandlordWithoutMarginStock[0] + nYearHouseProperty[0] - mortgageBalanceRemaining[0]];

  for (var i = 1; i < loanTerm; ++i) {
    if (shouldInflateRent) {
      totalAnnualNonHomeCost *= (1.0 + homeExpectedReturn);
    }
    // Renting
    nYearRentingStock.push(nYearRentingStock[i-1] * (1.0 + stockExpectedReturn) - totalAnnualNonHomeCost);

    // Buying House on Margin
    nYearHouseStock.push(nYearHouseStock[i-1] * (1.0 + stockExpectedReturn) - totalAnnualHomeOwningCost);
    nYearHouseProperty.push(nYearHouseProperty[i-1] * (1.0 + homeExpectedReturn));
    mortgageBalanceRemaining.push((monthlyMortgagePayment / monthlyMortgageInterestRate) * (1.0 - (1.0 / (1.0 + monthlyMortgageInterestRate)**(loanTermMonths - (12 * (i + 1))))));
    nYearHouseTotal.push(nYearHouseStock[i] + nYearHouseProperty[i] - mortgageBalanceRemaining[i] - marginValue);

    // No margin
    nYearNoMarginStock.push(nYearNoMarginStock[i-1] * (1.0 + stockExpectedReturn) - annualMortgageCost);
    nYearNoMarginTotal.push(nYearNoMarginStock[i] + nYearHouseProperty[i] - mortgageBalanceRemaining[i]);

    // Landlord
    nYearCumulativeRentReturns.push(nYearCumulativeRentReturns[i-1] + totalAnnualNonHomeCost);

    // Landlord With Margin
    nYearLandlordMarginStock.push(nYearLandlordMarginStock[i-1] * (1.0 + stockExpectedReturn) - totalAnnualHomeOwningCost + totalAnnualNonHomeCost)
    nYearLandlordMarginTotal.push(nYearLandlordMarginStock[i] + nYearHouseProperty[i] - mortgageBalanceRemaining[i] - marginValue);

    // Landlord Without Margin
    nYearLandlordWithoutMarginStock.push(nYearLandlordWithoutMarginStock[i-1] * (1.0 + stockExpectedReturn) - annualMortgageCost + totalAnnualNonHomeCost);
    nYearLandlordWithoutMarginTotal.push(nYearLandlordWithoutMarginStock[i] + nYearHouseProperty[i] - mortgageBalanceRemaining[i]);
  }

  var dataInput = [];
  for (var i = 1; i <= loanTerm; ++i) {
    var curr = [];
    curr.push(i);
    curr.push(nYearRentingStock[i-1]);
    curr.push(nYearHouseTotal[i-1]);
    curr.push(nYearNoMarginTotal[i-1]);
    curr.push(mortgageBalanceRemaining[i-1]);
    dataInput.push(curr);
  }

  var landlordGraphData = [];
  for (var i = 1; i <= loanTerm; ++i) {
    var curr = [];
    curr.push(i);
    curr.push(nYearCumulativeRentReturns[i-1]);
    curr.push(nYearLandlordMarginTotal[i-1]);
    curr.push(nYearLandlordWithoutMarginTotal[i-1]);
    curr.push(mortgageBalanceRemaining[i-1]);
    landlordGraphData.push(curr);
  }

  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Year');
  data.addColumn('number', 'Renting Value');
  data.addColumn('number', 'Net Owning w/ Margin Value');
  data.addColumn('number', 'Net Owning w/o Margin Value');
  data.addColumn('number', 'Mortgage Balance');

  var landlordData = new google.visualization.DataTable();
  landlordData.addColumn('number', 'Year');
  landlordData.addColumn('number', 'Cumulative Rent Returns (Separated)');
  landlordData.addColumn('number', 'Landlord With Margin Value');
  landlordData.addColumn('number', 'Landlord Without Margin Value');
  landlordData.addColumn('number', 'Mortgage Balance');

  data.addRows(dataInput);
  landlordData.addRows(landlordGraphData);

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
  var landlordChart = new google.visualization.LineChart(document.getElementById('LandlordReturnsGraph'));
  landlordChart.draw(landlordData, options);
}