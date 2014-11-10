%% Testing correlation between loc and %alc

X = [[4.95:0.01:5.05 ]+rand(1,11)*2 [9.95:0.01:10.05]+rand(1,11)*2];
Y = [[5.05:-0.01:4.95 ]+rand(1,11)*2 [10.05:-0.01:9.95]+rand(1,11)*2];
alc = [5+rand(1,11) 5.8+rand(1,11)];

[A,B,r,U,V,stats] = canoncorr(alc',[X' Y'])
figure;
plot(X,Y,'.','Color','g')
hold on;
plot(alc,'--')
plot(U,V,'.','Color','b')



b = regress(V,U) 
t = -2:10;
plot(t,b*t,'-.','Color','r')

legend('Position','%alc','UV', 'regression')