document.getElementById('video-nav').addEventListener('click', function(event) {
    event.preventDefault();

    var link = event.target;
    if(link.tagName.toLowerCase() !== 'a') return;

    var videoId = link.dataset.videoId;

    loadVideo(videoId);
});
function loadVideo(videoId) {
    var player = document.querySelector('#video-player video');
    if (!player) {
        player = document.createElement('video');
        player.controls = true;
        document.getElementById('video-player').appendChild(player);
    }
    var videoSources = {
        'video1':'',
        'video2':'',
        'video3':'https://flv1.gmw.cn/gma/20220503/20220503073752890_8084.m3u8',
        'video4':'',
        'video5':'',
    };
    player.src = '',
    player.load();
    player.play();
}