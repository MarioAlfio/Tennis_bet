% Carica il file
T = readtable("C:\Users\saraf\Downloads\tennis_data_cleaned.csv");

% Estrai e conta i livelli dei tornei
tourney_levels = categorical(T.tourney_level);
[grp, names] = findgroups(tourney_levels);
counts = splitapply(@numel, T.tourney_level, grp);

% Definisci i colori
bar_colors = [
    0.2 0.4 0.6;     % G: Grand Slam
    1.0 0.5 0.1;     % M: Masters 1000
    0.2 0.6 0.2;     % A: ATP 500/250
    0.9 0.2 0.2      % C: Challenger
];

% Crea il grafico
figure;
b = bar(counts, 'FaceColor', 'flat');
for i = 1:length(counts)
    b.CData(i,:) = bar_colors(i,:);
end
set(gca, 'XTickLabel', cellstr(names));
xlabel("Livello del Torneo");
ylabel("Conteggio");
title("Distribuzione dei Livelli dei Tornei");
legend(["G: Grand Slam", "M: Masters 1000", "A: ATP 500/250", "C: Challenger"], 'Location', 'northeastoutside');
