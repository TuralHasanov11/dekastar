window.addEventListener('DOMContentLoaded', event => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById('datatablesSimple');
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }

    const contactEmailDatatablesSimple = document.getElementById('contactEmailDatatablesSimple');
    if (contactEmailDatatablesSimple) {
        new simpleDatatables.DataTable(contactEmailDatatablesSimple);
    }

    const socialMediaLinkDatatablesSimple = document.getElementById('socialMediaLinkDatatablesSimple');
    if (socialMediaLinkDatatablesSimple) {
        new simpleDatatables.DataTable(socialMediaLinkDatatablesSimple);
    }

    const contactPhoneDatatablesSimple = document.getElementById('contactPhoneDatatablesSimple');
    if (contactPhoneDatatablesSimple) {
        new simpleDatatables.DataTable(contactPhoneDatatablesSimple);
    }
});
