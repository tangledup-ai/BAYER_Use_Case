/**
 * 昆明拜耳制药排班系统 - 通用JavaScript函数库
 * 提供全局工具函数和API调用接口
 */

/**
 * API基础URL配置
 * 根据实际部署环境调整
 */
const API_BASE_URL = '/api';

/**
 * 通用的fetch请求封装
 * @param {string} endpoint - API端点
 * @param {Object} options - fetch选项
 * @returns {Promise} 返回JSON数据
 */
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API请求失败:', error);
        throw error;
    }
}

/**
 * 显示通知消息
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型：success, error, warning, info
 * @param {number} duration - 显示时长（毫秒）
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        background: ${type === 'success' ? '#43e97b' : type === 'error' ? '#f5576c' : type === 'warning' ? '#fee140' : '#667eea'};
        color: ${type === 'warning' ? '#333' : 'white'};
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;

    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    if (!document.querySelector('style[data-notification="true"]')) {
        style.setAttribute('data-notification', 'true');
        document.head.appendChild(style);
    }

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, duration);
}

/**
 * 格式化日期
 * @param {string|Date} date - 日期对象或字符串
 * @param {string} format - 格式字符串
 * @returns {string} 格式化后的日期字符串
 */
function formatDate(date, format = 'YYYY-MM-DD') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');

    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} wait - 等待时间（毫秒）
 * @returns {Function} 防抖后的函数
 */
function debounce(func, wait = 300) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} limit - 时间限制（毫秒）
 * @returns {Function} 节流后的函数
 */
function throttle(func, limit = 300) {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

/**
 * 深拷贝对象
 * @param {Object} obj - 要拷贝的对象
 * @returns {Object} 拷贝后的对象
 */
function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }

    if (obj instanceof Date) {
        return new Date(obj.getTime());
    }

    if (obj instanceof Array) {
        return obj.map(item => deepClone(item));
    }

    if (obj instanceof Object) {
        const clonedObj = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                clonedObj[key] = deepClone(obj[key]);
            }
        }
        return clonedObj;
    }
}

/**
 * 数据导出功能
 * @param {Array} data - 要导出的数据
 * @param {string} filename - 文件名
 * @param {string} type - 导出类型：csv, json, xlsx
 */
function exportData(data, filename = 'data', type = 'csv') {
    let content = '';
    let mimeType = '';

    if (type === 'csv') {
        if (data.length > 0) {
            const headers = Object.keys(data[0]).join(',');
            const rows = data.map(item => Object.values(item).join(','));
            content = [headers, ...rows].join('\n');
        }
        mimeType = 'text/csv';
    } else if (type === 'json') {
        content = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${filename}.${type}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);

    showNotification('数据导出成功！', 'success');
}

/**
 * 表格数据验证
 * @param {Array} data - 要验证的数据
 * @param {Object} rules - 验证规则
 * @returns {Object} 验证结果
 */
function validateData(data, rules) {
    const errors = [];

    data.forEach((item, index) => {
        for (const field in rules) {
            const rule = rules[field];
            const value = item[field];

            if (rule.required && (!value && value !== 0)) {
                errors.push(`第${index + 1}行，字段"${field}"不能为空`);
                continue;
            }

            if (rule.type === 'number' && value && isNaN(Number(value))) {
                errors.push(`第${index + 1}行，字段"${field}"必须是数字`);
            }

            if (rule.min !== undefined && value < rule.min) {
                errors.push(`第${index + 1}行，字段"${field}"不能小于${rule.min}`);
            }

            if (rule.max !== undefined && value > rule.max) {
                errors.push(`第${index + 1}行，字段"${field}"不能大于${rule.max}`);
            }

            if (rule.pattern && !rule.pattern.test(value)) {
                errors.push(`第${index + 1}行，字段"${field}"格式不正确`);
            }
        }
    });

    return {
        valid: errors.length === 0,
        errors: errors
    };
}

/**
 * 本地存储管理
 */
const StorageManager = {
    /**
     * 设置数据到本地存储
     * @param {string} key - 键名
     * @param {any} value - 值
     */
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('本地存储失败:', e);
            return false;
        }
    },

    /**
     * 从本地存储获取数据
     * @param {string} key - 键名
     * @param {any} defaultValue - 默认值
     * @returns {any} 获取的值
     */
    get(key, defaultValue = null) {
        try {
            const value = localStorage.getItem(key);
            return value ? JSON.parse(value) : defaultValue;
        } catch (e) {
            console.error('读取本地存储失败:', e);
            return defaultValue;
        }
    },

    /**
     * 删除本地存储中的数据
     * @param {string} key - 键名
     */
    remove(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('删除本地存储失败:', e);
            return false;
        }
    },

    /**
     * 清空所有本地存储
     */
    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (e) {
            console.error('清空本地存储失败:', e);
            return false;
        }
    }
};

/**
 * 数字动画效果
 * @param {HTMLElement} element - 目标元素
 * @param {number} target - 目标数值
 * @param {number} duration - 动画时长（毫秒）
 */
function animateNumber(element, target, duration = 1000) {
    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (target - start) * easeProgress);

        element.textContent = current;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/**
 * 获取URL参数
 * @param {string} name - 参数名
 * @returns {string|null} 参数值
 */
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

/**
 * 设置URL参数
 * @param {Object} params - 参数对象
 */
function setUrlParameters(params) {
    const url = new URL(window.location);
    Object.keys(params).forEach(key => {
        url.searchParams.set(key, params[key]);
    });
    window.history.pushState({}, '', url);
}

/**
 * 认证和用户管理
 */
const AuthManager = {
    /**
     * 检查用户是否已登录。如果未登录且不是在登录页，则重定向到登录页。
     */
    checkAuth() {
        const user = StorageManager.get('user');
        const isLoginPage = window.location.pathname.endsWith('login.html');
        
        if (!user || !user.token) {
            if (!isLoginPage) {
                // Determine relative path back to root login page
                const depth = window.location.pathname.split('/').filter(p => p.length > 0).indexOf('pages') !== -1 ? 1 : 0;
                const pathPrefix = depth === 1 ? '../' : '';
                window.location.href = pathPrefix + 'login.html';
            }
            return null;
        }
        return user;
    },

    /**
     * 退出登录
     */
    logout() {
        StorageManager.remove('user');
        const depth = window.location.pathname.split('/').filter(p => p.length > 0).indexOf('pages') !== -1 ? 1 : 0;
        const pathPrefix = depth === 1 ? '../' : '';
        window.location.href = pathPrefix + 'login.html';
    },

    /**
     * 更新页面头部展示用户信息和退出按钮
     */
    updateHeader() {
        const user = this.checkAuth();
        if (!user) return;

        const header = document.querySelector('.header');
        if (header && !document.getElementById('userInfo')) {
            const userInfoDiv = document.createElement('div');
            userInfoDiv.id = 'userInfo';
            userInfoDiv.style.cssText = `
                display: flex;
                align-items: center;
                gap: 15px;
            `;

            const nameSpan = document.createElement('span');
            nameSpan.style.color = '#333';
            nameSpan.style.fontWeight = 'bold';
            nameSpan.innerHTML = `👋 你好, ${user.name} <small style="color:#666;font-weight:normal;">(${user.role === 'admin' ? '管理员' : '员工'})</small>`;

            const logoutBtn = document.createElement('button');
            logoutBtn.textContent = '退出登录';
            logoutBtn.className = 'btn btn-secondary';
            logoutBtn.style.padding = '5px 10px';
            logoutBtn.onclick = () => this.logout();

            userInfoDiv.appendChild(nameSpan);
            userInfoDiv.appendChild(logoutBtn);
            
            // Adjust header layout if necessary
            header.style.display = 'flex';
            header.style.justifyContent = 'space-between';
            header.style.alignItems = 'center';
            header.style.flexWrap = 'wrap';

            header.appendChild(userInfoDiv);
        }
    }
};

/**
 * 导出为全局函数，供HTML页面使用
 */
window.fetchAPI = fetchAPI;
window.showNotification = showNotification;
window.formatDate = formatDate;
window.debounce = debounce;
window.throttle = throttle;
window.deepClone = deepClone;
window.exportData = exportData;
window.validateData = validateData;
window.StorageManager = StorageManager;
window.animateNumber = animateNumber;
window.getUrlParameter = getUrlParameter;
window.setUrlParameters = setUrlParameters;
window.AuthManager = AuthManager;
