package ca.cmpt383.project.controller;

import org.springframework.boot.autoconfigure.web.servlet.DispatcherServletAutoConfiguration;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.DispatcherServlet;
import org.springframework.web.servlet.config.annotation.*;

@Configuration
public class WebMvcConfig implements WebMvcConfigurer {
    @Bean(name = DispatcherServletAutoConfiguration.DEFAULT_DISPATCHER_SERVLET_BEAN_NAME)
    public DispatcherServlet dispatcherServlet() {
        DispatcherServlet dispatcherServlet = new DispatcherServlet();
        dispatcherServlet.setDetectAllHandlerAdapters(true);
        dispatcherServlet.setDetectAllHandlerExceptionResolvers(true);
        dispatcherServlet.setDetectAllHandlerMappings(true);
        dispatcherServlet.setDetectAllViewResolvers(true);
        dispatcherServlet.setThrowExceptionIfNoHandlerFound(true);
        return dispatcherServlet;
    }
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOriginPatterns("*") // adapted from https://github.com/spring-projects/spring-framework/issues/26111
                .allowCredentials(true)
        ;
    }
}