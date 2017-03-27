clear all
close all

img = imread('DepartmentStoreW.jpg');
imshow(img);
newwaldo = rgb2gray(img);
title('input');

% cropping wally in the original image
height = 50;
width = height;
stx = 151;
sty = 143;
wally = img((sty):(sty+height), (stx):(stx+width), :);
figure, imshow(wally);
imwrite(wally, 'wally_department.jpg');
newface = rgb2gray(wally);

% now you can find out wally
locx = 1;
locy = 1;
width = size(wally, 2);
height = size(wally, 1);

%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%
cc=normxcorr2(newface,newwaldo);
figure(5);
surf(cc), shading flat

[max_c,imax]=max(abs(cc(:)));
[locy,locx]=ind2sub(size(cc),imax(1));
% draw your result
output = img;
figure, imshow(output), hold on
rectangle('position',[(locx-50) (locy-50) 75 75],'LineWidth',4,'EdgeColor','b');
%plot([locx locx], [locy locy+width], 'b', 'LineWidth', 3);
%plot([locx locx+height], [locy locy], 'b', 'LineWidth', 3);
%plot([locx+height locx+height], [locy locy+width], 'b', 'LineWidth', 3);
%plot([locx locx+height], [locy+width locy+width], 'b', 'LineWidth', 3);
title('output');
