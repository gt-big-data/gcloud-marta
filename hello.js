module.exports = {
    helloWorld: (req, res) => {
        res.send(`Hello ${req.body.name || 'World'}!`);
    };
}