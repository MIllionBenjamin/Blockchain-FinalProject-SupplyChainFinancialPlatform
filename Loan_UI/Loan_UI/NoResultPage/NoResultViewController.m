//
//  UIViewController+NoResultViewController.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/13.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "NoResultViewController.h"
#import "AppDelegate.h"
#import "Masonry.h"
#import "AFNetworking.h"

@interface NoResultViewController () {
    NSInteger itemWidth;
}


@end

@implementation NoResultViewController


- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self.view addSubview: self.errorLabel];
    
    //inset distance to (top, left, bottom, right)
    /*
    UIEdgeInsets inset_title = UIEdgeInsetsMake(200, 100, 600, 100);
    [self.errorLabel mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_title);
    }];
     */
    
}


- (UILabel *)errorLabel {
    if(_errorLabel == nil) {
        _errorLabel = [[UILabel alloc] init];
        NSInteger itemWidth = 200;
        [_errorLabel setFont: [UIFont systemFontOfSize: 23]];
        [_errorLabel setText:@"无对应结果！"];
        [_errorLabel setTextColor:[UIColor systemRedColor]];
        _errorLabel.frame = CGRectMake(self.view.frame.size.width / 2 - itemWidth / 2, 280,  itemWidth, 40);
        [_errorLabel setTextAlignment:NSTextAlignmentCenter];
    }
    return _errorLabel;
}





@end


