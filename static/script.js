document.addEventListener('DOMContentLoaded', () => {
    // Initialize Highlight.js
    hljs.highlightAll();

    const generateBtn = document.getElementById('generateBtn');
    const promptInput = document.getElementById('promptInput');
    const codeEditor = document.getElementById('codeEditor');
    const fileNameBadge = document.getElementById('fileNameBadge');

    // Status
    const systemStatusText = document.querySelector('#systemStatus .status-text');
    const systemStatusBadge = document.getElementById('systemStatus');

    const testStatusInd = document.getElementById('testStatusIndicator');
    const testOutput = document.getElementById('testOutput');
    const deployStatusInd = document.getElementById('deployStatusIndicator');
    const deployOutput = document.getElementById('deployOutput');
    const launchActionBox = document.getElementById('launchActionBox');
    const viewOutputBtn = document.getElementById('viewOutputBtn');

    // Steps
    const steps = {
        wait: document.getElementById('stepWait'),
        gen: document.getElementById('stepGen'),
        test: document.getElementById('stepTest'),
        deploy: document.getElementById('stepDeploy')
    };

    // Connectors
    const connectors = document.querySelectorAll('.step-connector');

    function resetUI() {
        // Reset steps to pending, except wait which is completed instantly
        Object.values(steps).forEach(step => {
            step.className = 'step-item pending';
        });

        connectors.forEach(c => c.className = 'step-connector');

        // Clear outputs
        codeEditor.textContent = '# The AI Software Engineer is thinking...\n# Generating optimal solution...';
        hljs.highlightElement(codeEditor);
        fileNameBadge.textContent = 'workspace/processing...';

        // Reset result panels
        if (testOutput) {
            testOutput.className = 'terminal-box';
            testOutput.textContent = 'Waiting for execution...';
        }
        if (testStatusInd) {
            testStatusInd.className = 'status-indicator';
            testStatusInd.textContent = 'Pending';
        }

        // Reset deploy panels
        if (deployOutput) {
            deployOutput.className = 'terminal-box';
            deployOutput.textContent = 'Waiting for deployment phase...';
        }
        if (deployStatusInd) {
            deployStatusInd.className = 'status-indicator';
            deployStatusInd.textContent = 'Pending';
        }

        // Hide launch action until ready
        if (launchActionBox) {
            launchActionBox.classList.add('hidden');
        }

        // Set working status
        systemStatusText.textContent = 'Working...';
        systemStatusBadge.className = 'status-badge working';
    }

    function setStepStatus(stepKey, status, connectorIndex = -1) {
        if (steps[stepKey]) {
            steps[stepKey].className = `step-item ${status}`;
        }
        if (status === 'completed' && connectorIndex >= 0 && connectorIndex < connectors.length) {
            connectors[connectorIndex].classList.add('completed');
        }
    }

    generateBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        if (!prompt) {
            alert("Please enter a feature request first.");
            return;
        }

        // BTN loading state
        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-content').classList.add('hidden');
        generateBtn.querySelector('.btn-loader').classList.add('active');

        resetUI();
        setStepStatus('wait', 'completed', 0);
        setStepStatus('gen', 'active');

        try {
            const response = await fetch('/api/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: prompt })
            });

            const data = await response.json();

            // RESILIENCE: Process generation results if they exist, even if error occurred later
            if (data.results && data.results.generation) {
                setStepStatus('gen', 'completed', 1);
                codeEditor.textContent = data.results.generation.code;
                hljs.highlightElement(codeEditor);
                fileNameBadge.textContent = `workspace/${data.results.generation.filename}`;
            }

            if (!response.ok) {
                // Determine which step failed and update UI
                if (data.step === 'generation') setStepStatus('gen', 'error');

                if (data.step === 'testing') {
                    setStepStatus('test', 'error');
                    if (testOutput && data.results && data.results.testing) {
                        testOutput.textContent = data.results.testing.output || data.results.testing.message;
                        testOutput.classList.add('error');
                    }
                    if (testStatusInd) {
                        testStatusInd.textContent = 'Failed';
                        testStatusInd.classList.add('error');
                    }
                }

                if (data.step === 'deployment') setStepStatus('deploy', 'error');

                throw new Error(data.error || data.message || "Pipeline Failed");
            }

            // If we reach here, it's successful
            // 2. Testing Phase
            setStepStatus('test', 'active');

            if (data.results.testing) {
                testOutput.textContent = data.results.testing.output || data.results.testing.message;

                if (data.results.testing.status === 'success') {
                    testOutput.classList.add('success');
                    testStatusInd.textContent = 'Passed';
                    testStatusInd.classList.add('success');
                    setStepStatus('test', 'completed', 2);

                    if (launchActionBox) launchActionBox.classList.remove('hidden');
                    if (viewOutputBtn) viewOutputBtn.classList.remove('hidden');
                } else {
                    testOutput.classList.add('error');
                    testStatusInd.textContent = 'Failed';
                    testStatusInd.classList.add('error');
                    setStepStatus('test', 'error');
                }
            }

            // 3. Deployment Phase
            setStepStatus('deploy', 'active');

            if (data.results.deployment) {
                deployOutput.textContent = data.results.deployment.log || data.results.deployment.message;

                if (data.results.deployment.status === 'success') {
                    deployOutput.classList.add('success');
                    deployStatusInd.textContent = 'Success';
                    deployStatusInd.classList.add('success');
                    setStepStatus('deploy', 'completed');
                } else {
                    deployOutput.classList.add('error');
                    deployStatusInd.textContent = 'Failed';
                    deployStatusInd.classList.add('error');
                    setStepStatus('deploy', 'error');
                }
            }

            systemStatusText.textContent = 'Ready';
            systemStatusBadge.className = 'status-badge';

        } catch (error) {
            console.error("Pipeline Error:", error);
            systemStatusText.textContent = 'Error';
            systemStatusBadge.className = 'status-badge error';
        } finally {
            generateBtn.disabled = false;
            generateBtn.querySelector('.btn-content').classList.remove('hidden');
            generateBtn.querySelector('.btn-loader').classList.remove('active');
        }
    });

    if (viewOutputBtn) {
        viewOutputBtn.addEventListener('click', () => {
            const resultsPanel = document.getElementById('resultsPanel');
            if (resultsPanel) resultsPanel.scrollIntoView({ behavior: 'smooth' });
        });
    }

    const launchAppBtn = document.getElementById('launchAppBtn');
    if (launchAppBtn) {
        launchAppBtn.addEventListener('click', () => {
            const fullFilename = fileNameBadge.textContent || '';
            const filename = fullFilename.split('/').pop();
            if (filename && filename !== 'waiting...' && filename !== 'processing...') {
                window.open(`/view_result/${filename}`, '_blank');
            }
        });
    }
});
