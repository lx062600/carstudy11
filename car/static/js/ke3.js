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
        'video1':'http://hw-jiakao-video.jiakaobaodian.com/knowhere/2021/03/09/861de9d5d0644534a521f846ee8ca62b.middle.mp4?auth_key=1718621094-26a9420fe790486a86d25854dca31c67-0-523c81667b6c3b07dbd8631190e01ce8',
        'video3':'',
        'video4':'',
        'video5':'',
        'video6':'',
        'video7':'',
        'video8':'',
        'video9':'',
        'video10':'',
        'video11':'',
        'video12':'',
        'video13':'',
        'video14':'',
    };
    player.src = '',
    player.load();
    player.play();
}
