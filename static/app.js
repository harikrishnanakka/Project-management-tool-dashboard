document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/tasks/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(projects => {
            console.log('Fetched projects:', projects); // Debugging line to check the fetched data

            // Check if projects array is valid
            if (!Array.isArray(projects)) {
                throw new Error('Invalid data format: projects is not an array');
            }

            // Filter projects based on their status
            const projectProgressData = projects.map(project => {
                let progress = 0;
                if (project.status === 'done') {
                    progress = 100;
                }
                return {
                    name: project.name,
                    progress: progress
                };
            });

            console.log('Processed project progress data:', projectProgressData); // Debugging line to check the processed data

            // Ensure we have valid data to plot
            if (projectProgressData.length === 0) {
                throw new Error('No project data available to plot');
            }

            // Plot the completion percentage for each project
            const data = {
                x: projectProgressData.map(project => project.name),
                y: projectProgressData.map(project => project.progress),
                type: 'bar'
            };

            const layout = {
                title: "Team tasks completion %",
                xaxis: {
                    title: 'Projects'
                },
                yaxis: {
                    title: 'Completion %',
                    range: [0, 100]
                }
            };

            Plotly.newPlot('project-progress-graph', [data], layout);
        })
        .catch(error => console.error('Error fetching or plotting projects:', error));
});









    


function changeMonth(monthChange) {
    const currentMonth = document.getElementById('current-month').innerText;
    const [month, year] = currentMonth.split(' ');
    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const currentMonthIndex = monthNames.indexOf(month);
    let newMonthIndex = currentMonthIndex + monthChange;
    let newYear = parseInt(year);
    if (newMonthIndex < 0) {
        newMonthIndex = 11;
        newYear--;
    } else if (newMonthIndex > 11) {
        newMonthIndex = 0;
        newYear++;
    }
    const newMonth = monthNames[newMonthIndex];
    document.getElementById('current-month').innerText = `${newMonth} ${newYear}`;

    // Clear the existing dates
    const daysList = document.querySelector('.days');
    daysList.innerHTML = '';

    // Get the number of days in the new month
    const daysInMonth = new Date(newYear, newMonthIndex + 1, 0).getDate();

    // Populate the days list with the dates for the new month
    for (let i = 1; i <= daysInMonth; i++) {
        const listItem = document.createElement('li');
        listItem.textContent = i;
        daysList.appendChild(listItem);
    }
}

// Initial call to populate the calendar with dates for the current month
changeMonth(0);


document.addEventListener('DOMContentLoaded', function() {
fetch('/api/tasks/')
.then(response => response.json())
.then(tasks => {
    let taskTimelineData = tasks.map(task => ({
        x: task.deadline,
        y: task.name,
        type: 'scatter',
        mode: 'markers'
    }));

    Plotly.newPlot('task-timeline', taskTimelineData);
})
.catch(error => console.error('Error fetching tasks:', error));
});




document.addEventListener('DOMContentLoaded', function() {
fetch('/api/projects/')
    .then(response => response.json())
    .then(projects => {
        let totalProgress = 0;

        const projectPromises = projects.map(project =>
            fetch(`/api/projects/${project.id}/progress/`)
                .then(response => response.json())
        );

        Promise.all(projectPromises)
            .then(progressDataArray => {
                progressDataArray.forEach(progressData => {
                    totalProgress += progressData.progress;
                });

                // Calculate the overall completion percentage
                const overallCompletionPercentage = totalProgress / projects.length;

                // Render the overall completion percentage graph
                Plotly.newPlot('project-completion-graph', [{
                    x: ['Overall Completion'],
                    y: [overallCompletionPercentage],
                    type: 'bar',
                    text: [`${overallCompletionPercentage.toFixed(2)}%`],
                    textposition: 'auto',
                    marker: {
                        color: 'rgba(50,171,96,0.6)',
                        line: {
                            color: 'rgba(50,171,96,1.0)',
                            width: 2
                        }
                    }
                }], {
                    title: 'Overall Project Completion Percentage',
                    yaxis: {
                        range: [0, 100],
                        title: 'Completion %'
                    }
                });
            })
            .catch(error => console.error('Error fetching project progress:', error));
    })
    .catch(error => console.error('Error fetching projects:', error));
});




document.addEventListener('DOMContentLoaded', function() {
Promise.all([
    fetch('/api/projects/').then(response => response.json()),
    fetch('/api/tasks/').then(response => response.json())
]).then(([projects, tasks]) => {
    // Extract task timelines from projects
    const taskTimelineData = projects.map(project => {
        const tasksInProject = tasks.filter(task => task.project === project.id);
        return {
            projectId: project.id,
            projectName: project.name,
            tasks: tasksInProject.map(task => ({
                taskId: task.id,
                taskName: task.name,
                startDate: task.start_date,
                endDate: task.end_date,
                deadline: task.deadline,
                status: task.status
            }))
        };
    });

    // Plot the task timelines
    taskTimelineData.forEach(project => {
        const projectTasks = project.tasks.map(task => ({
            x: [task.startDate, task.endDate], // Use an array to support multiple traces
            y: [task.taskName, task.taskName],
            type: 'scatter',
            mode: 'lines',
            name: task.taskName, // Task name as trace name
            line: {
                width: 5 // Set line width for better visibility
            }
        }));

        // Add markers for task deadlines and milestones
        const markers = project.tasks.flatMap(task => {
            const markerArray = [];
            if (task.deadline) {
                markerArray.push({
                    x: [task.deadline],
                    y: [task.taskName],
                    type: 'scatter',
                    mode: 'markers',
                    marker: {
                        symbol: 'diamond',
                        size: 8,
                        color: 'green'
                    },
                    name: `${task.taskName} - Deadline`
                });
            }
            if (task.status.toLowerCase() === 'done') {
                markerArray.push({
                    y: [task.taskName],
                    type: 'scatter',
                    mode: 'markers',
                    marker: {
                        symbol: 'star',
                        size: 8,
                        color: 'blue'
                    },
                    name: `${task.taskName} - Milestone`
                });
            }
            return markerArray;
        });

        // Combine project tasks and markers
        const combinedData = projectTasks.concat(markers);

        // Add layout configuration
        const layout = {
            title: `${project.projectName} Task Timeline`,
            xaxis: {
                title: 'Date',
                type: 'date', // Ensure the x-axis is treated as dates
                tickformat: '%d-%m' // Format to display only day and month
            },
            yaxis: {
                title: 'Task Name'
            }
        };

        // Plot the task timeline for each project
        Plotly.newPlot('task-timeline', combinedData, layout);
    });
}).catch(error => console.error('Error fetching data:', error));
});