% Carica il dataset
T = readtable("C:\Users\saraf\Downloads\tennis_data_cleaned.csv");

% Filtra le righe con valori mancanti nelle due variabili
validRows = ~isnan(T.w_ace_rate) & ~isnan(T.w_dominance_ratio);
x = T.w_ace_rate(validRows);  % Variabile indipendente (asse x)
y = T.w_dominance_ratio(validRows);  % Variabile dipendente (asse y)

% Scatterplot
figure;
scatter(x, y, 25, 'filled', 'MarkerFaceAlpha', 0.5);
xlabel('Tasso di Ace (%)');
ylabel('Dominance Ratio');
title('Scatterplot: Tasso di Ace vs Dominance Ratio');

% Calcolo della correlazione (Pearson)
[r, p] = corr(x, y, 'Type', 'Pearson');
text(max(x)*0.6, max(y)*0.9, sprintf('r = %.2f, p = %.4f', r, p), 'FontSize', 12);

% Regressione lineare
coeff = polyfit(x, y, 1); % coeff(1) = slope, coeff(2) = intercept
xFit = linspace(min(x), max(x), 100);
yFit = polyval(coeff, xFit);
hold on;
plot(xFit, yFit, 'r-', 'LineWidth', 2);
legend('Match', 'Retta di regressione', 'Location', 'best');

grid on;
