clear all
close all
clc

minx = 0;
miny = 0;
maxx = 1000;
maxy = 1000;
incrementx = 5;
incrementy = 5;
Zfliptot = zeros((maxx-minx)/incrementx+1, (maxy-miny)/incrementy+1);

for i=1:6
    
    close all
    clearvars -except i Zfliptot minx maxx miny maxy incrementx incrementy
    
    if i == 1
        isotope = char('131m');
        Xedges = minx:incrementx:maxx;
        Yedges = miny:incrementy:maxy;
    elseif i == 2
        isotope = char('133m');
        Xedges = minx:incrementx:maxx;
        Yedges = miny:incrementy:maxy;
    elseif i == 3
        isotope = char('135');        
        Xedges = minx:incrementx:maxx;
        Yedges = miny:incrementy:maxy;
    elseif i == 4
        isotope = char('133gb');
        Xedges = minx:incrementx:maxx;
        Yedges = miny:incrementy:maxy;
    elseif i == 5
        isotope = char('133xb');
        Xedges = minx:incrementx:maxx;
        Yedges = miny:incrementy:maxy;
    elseif i == 6
        isotope = char('133xe');
        Xedges = minx:incrementx:maxx;
        Yedges = miny:incrementy:maxy;
    end
        
    fileID = fopen([isotope, '_coin.txt'],'r');            %read in file
    columns = textscan(fileID,'%s %s %s %s');   %scan file info into 4 columns

    % ID = cellfun(@str2num,(columns{1,1}(2:end,1)));
    % nps = cellfun(@str2num,(columns{1,2}(2:end,1)));

    energy(:,1) = cellfun(@str2num,(columns{1,3}(2:end,1)))*1000;   %photon
    energy(:,2) = cellfun(@str2num,(columns{1,4}(2:end,1)))*1000;   %electron
    broadenedenergy = normrnd(energy,(0.17/2.35)*energy);           %apply gaussian broadening

    Z=hist3(broadenedenergy, 'ctrs', {Yedges Xedges});
    h=surfc(Xedges,Yedges,Z);
    axis xy
    view(2)
    set(h,'LineStyle','none')
    set(gca, 'FontSize', 14)
    colorbar
    colormap jet
    xlabel('Energy (kev), Silicon 1 + Silicon 2','Fontsize', 14);
    ylabel('Energy (kev), CZT 1 + CZT 2','Fontsize', 14);
    title([isotope, 'Xe electron-photon Coincidence'],'FontSize', 14, 'fontweight','bold');
    axis square

    saveas(gcf,[isotope, '_plot.png']);
    saveas(gcf,[isotope, '_plot.fig']);
    save([isotope, '_histogram.mat'])
    Zflip = flipud(Z);
    csvwrite(['test', num2str(i+23), '.csv'],Zflip)

    Zfliptot=Zfliptot+Zflip;
    
    isotope
    
end

csvwrite(['test', num2str(i+1+23), '.csv'],Zfliptot)