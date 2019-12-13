//
//  AppDelegate.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/12.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "AppDelegate.h"
#import "InitialViewController.h"

@interface AppDelegate ()

@end

@implementation AppDelegate


- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    // Override point for customization after application launch.
    self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
    //self.vc = [[InitialViewController alloc] init];
    InitialViewController* vc = [[InitialViewController alloc] init];
    self.window.backgroundColor = [UIColor whiteColor];
    [vc viewDidLoad];
    [self.window makeKeyAndVisible];
    
    self.nc = [[UINavigationController alloc] initWithRootViewController:vc];
    //self.nc.navigationBar.hidden = YES;
    
    self.window.rootViewController = self.nc;
    
    
    return YES;
}

/*
#pragma mark - UISceneSession lifecycle


- (UISceneConfiguration *)application:(UIApplication *)application configurationForConnectingSceneSession:(UISceneSession *)connectingSceneSession options:(UISceneConnectionOptions *)options {
    // Called when a new scene session is being created.
    // Use this method to select a configuration to create the new scene with.
    return [[UISceneConfiguration alloc] initWithName:@"Default Configuration" sessionRole:connectingSceneSession.role];
}


- (void)application:(UIApplication *)application didDiscardSceneSessions:(NSSet<UISceneSession *> *)sceneSessions {
    // Called when the user discards a scene session.
    // If any sessions were discarded while the application was not running, this will be called shortly after application:didFinishLaunchingWithOptions.
    // Use this method to release any resources that were specific to the discarded scenes, as they will not return.
}
*/

@end
