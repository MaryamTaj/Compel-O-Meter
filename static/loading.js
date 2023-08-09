document.addEventListener('DOMContentLoaded', function() {
    var loadingOverlay = document.getElementById('loadingOverlay')
    loadingOverlay.style.display = 'none'

    window.addEventListener('beforeunload', function() {
        loadingOverlay.style.display = 'block'
    })
})
