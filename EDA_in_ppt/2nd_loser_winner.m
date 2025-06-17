% Carica i dati con i nomi originali delle colonne
T = readtable("C:/Users/saraf/Downloads/tennis_data_cleaned.csv", ...
    'VariableNamingRule', 'preserve');

% Converti le due colonne da stringa a numerico
w_2nd_raw = T.w_2nd_pct;
l_2nd_raw = T.l_2nd_pct;

% Controllo: verifica se sono stringhe o numeri
if iscell(w_2nd_raw) || isstring(w_2nd_raw)
    w_2nd = str2double(strrep(w_2nd_raw, ',', '.'));
else
    w_2nd = w_2nd_raw;
end

if iscell(l_2nd_raw) || isstring(l_2nd_raw)
    l_2nd = str2double(strrep(l_2nd_raw, ',', '.'));
else
    l_2nd = l_2nd_raw;
end

% Pulisci: rimuovi NaN
w_2nd = w_2nd(~isnan(w_2nd));
l_2nd = l_2nd(~isnan(l_2nd));

% Controllo: stampa numero di valori validi
fprintf("Valori validi (w_2nd): %d\n", numel(w_2nd));
fprintf("Valori validi (l_2nd): %d\n", numel(l_2nd));

% Controlla che ci siano abbastanza dati
if isempty(w_2nd) || isempty(l_2nd)
    error("Una delle due variabili è vuota: impossibile calcolare la densità.");
end

% Plot
figure;
hold on;

% Istogrammi
histogram(w_2nd, 'Normalization','pdf', ...
    'FaceColor', [0.2 0.6 1], 'EdgeColor','none', 'FaceAlpha', 0.6);
histogram(l_2nd, 'Normalization','pdf', ...
    'FaceColor', [1 0.5 0.2], 'EdgeColor','none', 'FaceAlpha', 0.6);

% Densità
[f_w, x_w] = ksdensity(w_2nd);
plot(x_w, f_w, 'b', 'LineWidth', 2);

[f_l, x_l] = ksdensity(l_2nd);
plot(x_l, f_l, 'Color', [1 0.3 0], 'LineWidth', 2);

% Titoli
title('Distribuzione % Punti Vinti sulla Seconda – Vincitore vs Perdente');
xlabel('Percentuale di Punti Vinti sulla 2a (%)');
ylabel('Densità');
legend('Vincitore', 'Perdente', 'Densità Vincitore', 'Densità Perdente');

grid on;
