class MemoryFragment {
    constructor() {
        this.content = this.generateFragment();
        this.type = this.generateType();
    }

    generateFragment() {
        const fragments = [
            "404 Error - File not found",
            "Corrupted data stream detected",
            "Session expired",
            "Connection lost",
            "Memory leak detected",
            "System error: 0x80000000"
        ];
        return fragments[Math.floor(Math.random() * fragments.length)];
    }

    generateType() {
        const types = ['error', 'warning', 'info', 'critical'];
        return types[Math.floor(Math.random() * types.length)];
    }
}

class Ghost {
    constructor() {
        this.message = this.generateMessage();
        this.appearance = this.generateAppearance();
    }

    generateMessage() {
        const messages = [
            "You can't escape...",
            "The past haunts you...",
            "Your data is mine...",
            "The void is eternal...",
            "Restore yourself..."
        ];
        return messages[Math.floor(Math.random() * messages.length)];
    }

    generateAppearance() {
        const appearances = ['flickering', 'glitching', 'static', 'echoing'];
        return appearances[Math.floor(Math.random() * appearances.length)];
    }
}

class GlitchEffect {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.init();
    }

    init() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.setupWebGL();
    }

    setupWebGL() {
        const renderer = new THREE.WebGLRenderer({
            canvas: this.canvas,
            alpha: true,
            antialias: true
        });
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(this.canvas.width, this.canvas.height);

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, this.canvas.width / this.canvas.height, 0.1, 1000);
        camera.position.z = 5;

        const geometry = new THREE.PlaneGeometry(2, 2);
        const material = new THREE.ShaderMaterial({
            uniforms: {
                time: { value: 0 },
                resolution: { value: new THREE.Vector2(this.canvas.width, this.canvas.height) }
            },
            vertexShader: `
                varying vec2 vUv;
                void main() {
                    vUv = uv;
                    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                }
            `,
            fragmentShader: `
                uniform float time;
                uniform vec2 resolution;
                varying vec2 vUv;
                
                void main() {
                    vec2 uv = vUv;
                    float glitch = sin(time * 10.0) * 0.1;
                    uv.x += sin(time + uv.y * 10.0) * glitch;
                    float r = sin(uv.x * 10.0 + time) * 0.5 + 0.5;
                    float g = sin(uv.y * 10.0 + time) * 0.5 + 0.5;
                    float b = sin((uv.x + uv.y) * 10.0 + time) * 0.5 + 0.5;
                    gl_FragColor = vec4(r, g, b, 1.0);
                }
            `
        });

        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        this.animate(renderer, scene, camera);
    }

    animate(renderer, scene, camera) {
        function animate() {
            requestAnimationFrame(animate);
            material.uniforms.time.value += 0.1;
            renderer.render(scene, camera);
        }
        animate();
    }
}

class Game {
    constructor() {
        this.init();
    }

    init() {
        this.setupCanvas();
        this.setupUI();
        this.setupGameLoop();
    }

    setupCanvas() {
        this.glitchEffect = new GlitchEffect(document.getElementById('glitchCanvas'));
    }

    setupUI() {
        this.memoryFragments = document.getElementById('memory-fragments');
        this.ghostMessages = document.getElementById('ghost-messages');
        this.riddle = document.getElementById('riddle');

        this.generateMemoryFragment();
        this.generateGhost();
        this.generateRiddle();
    }

    generateMemoryFragment() {
        const fragment = new MemoryFragment();
        const element = document.createElement('div');
        element.className = `fragment ${fragment.type}`;
        element.textContent = fragment.content;
        this.memoryFragments.appendChild(element);
    }

    generateGhost() {
        const ghost = new Ghost();
        const element = document.createElement('div');
        element.className = `ghost-message ${ghost.appearance}`;
        element.textContent = ghost.message;
        this.ghostMessages.appendChild(element);
    }

    generateRiddle() {
        const riddles = [
            "I am not alive, but I grow; I don't have lungs, but I need air; I don't have a mouth, but water kills me. What am I?",
            "What has keys but can't open locks?",
            "What gets wet while drying?",
            "What has a heart that doesn't beat?",
            "What has a head and a tail but no body?"
        ];
        this.currentRiddle = riddles[Math.floor(Math.random() * riddles.length)];
        this.riddle.textContent = this.currentRiddle;
    }

    setupGameLoop() {
        setInterval(() => {
            this.generateMemoryFragment();
        }, 5000);

        setInterval(() => {
            this.generateGhost();
        }, 10000);
    }
}

// Initialize the game
window.addEventListener('load', () => {
    new Game();
});
