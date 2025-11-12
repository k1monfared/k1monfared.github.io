$(document).ready(function() {
    function ChangeImageSize(Element, targetWidth) {
        //alert ('Change Size of ' + Element.ID + ' to ' + targetWidth);

        var newTargetWidth;

        if (targetWidth > 0.5) { //double it
            Element.height *= 2;
            Element.width *= 2;
            newTargetWidth = targetWidth / 2;
        } else { //half it
            Element.height *= .5;
            Element.width *= .5;
            newTargetWidth = targetWidth * 2;
        }

        Element.onclick = 'ChangeImageSize(this, ' + newTargetWidth + ')'; //  Changed it from Element.id to this

    }
});
