% Carica il file
T = readtable("C:\Users\saraf\Downloads\tennis_data_cleaned.csv");

% Estrai e conta i turni di gioco
rounds = categorical(T.round);
[grp, names] = findgroups(rounds);
counts = splitapply(@numel, T.round, grp);

% Ordine desiderato dei turni
ordine_round = ["Q1","Q2","Q3","R64","R32","R16","QF","SF","F"];
[counts_sorted, idx] = ismember(ordine_round, cellstr(names));
counts_ordered = zeros(size(ordine_round));
for i = 1:length(idx)
    if idx(i) ~= 0
        counts_ordered(i) = counts(idx(i));
    end
end

% Colori automatici
bar_colors = lines(length(ordine_round));

% Crea il grafico
figure;
b = bar(counts_ordered, 'FaceColor', 'flat');
for i = 1:length(ordine_round)
    b.CData(i,:) = bar_colors(i,:);
end

set(gca, 'XTickLabel', ordine_round);
xlabel("Turno");
ylabel("Conteggio");
title("Distribuzione dei Turni di Gioco");
legend({
    "Q1: Primo turno di qualificazione", ...
    "Q2: Secondo turno di qualificazione", ...
    "Q3: Terzo turno di qualificazione", ...
    "R64: Primo turno (64 giocatori)", ...
    "R32: Secondo turno (32 giocatori)", ...
    "R16: Ottavi di finale", ...
    "QF: Quarti di finale", ...
    "SF: Semifinali", ...
    "F: Finale"
}, 'Location', 'northeastoutside');