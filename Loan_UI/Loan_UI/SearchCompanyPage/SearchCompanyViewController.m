//
//  UICollectionViewController+SearchCompanyPage.m
//  Loan_UI
//
//  Created by MillionBenjamin on 2019/12/13.
//  Copyright © 2019 中山大学. All rights reserved.
//

#import "SearchCompanyViewController.h"
#import "AppDelegate.h"
#import "Masonry.h"
#import "AFNetworking.h"
#import "CompanyResultViewController.h"
#import "NoResultViewController.h"

@interface SearchCompanyViewController ()

@end

@implementation SearchCompanyViewController

- (void)viewWillAppear:(BOOL)animated {
    [super viewWillAppear:YES];
    [self.view addSubview:self.inputField];
    /*
    UIEdgeInsets inset_input = UIEdgeInsetsMake(230, 100, 600, 100);
    
    [self.guideLabel mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_input);
    }];
     */

}


- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self.view addSubview: self.guideLabel];
    //inset distance to (top, left, bottom, right)
    UIEdgeInsets inset_title = UIEdgeInsetsMake(200, 100, 600, 100);
    [self.guideLabel mas_makeConstraints:^(MASConstraintMaker *make){
        make.edges.equalTo(self.view).with.insets(inset_title);
    }];
    
    [self.view addSubview: self.confirmButton];
    

}


- (UILabel *)guideLabel {
    if(_guideLabel == nil) {
        _guideLabel = [[UILabel alloc] init];
        [_guideLabel setText: @"请输入公司名称"];
        [_guideLabel setFont: [UIFont systemFontOfSize: 23]];
        [_guideLabel setTextColor: [UIColor blackColor]];
        [_guideLabel setTextAlignment:NSTextAlignmentCenter];
        //_guideLabel.backgroundColor = [UIColor blueColor];
    }
    return _guideLabel;
}


- (UITextField *)inputField {
    if(_inputField == nil) {
        NSInteger fieldWidth = 275;
        _inputField = [[UITextField alloc]initWithFrame:CGRectMake(self.view.frame.size.width / 2 - fieldWidth / 2, 300, fieldWidth, 40)];
        _inputField.borderStyle = UITextBorderStyleRoundedRect;
        _inputField.backgroundColor = [UIColor whiteColor];
        _inputField.placeholder = @"公司名称";
        _inputField.font = [UIFont systemFontOfSize:20];
        _inputField.clearButtonMode = UITextFieldViewModeAlways;
        _inputField.autocapitalizationType = UITextAutocapitalizationTypeNone;
        //_inputField.textAlignment = NSTextAlignmentCenter;
    }
    return _inputField;
}


- (UIButton*)confirmButton {
    if (_confirmButton == nil) {
        
        _confirmButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
        _confirmButton.clipsToBounds = YES;
        [_confirmButton.layer setCornerRadius:10.0];
        [_confirmButton.layer setMasksToBounds:YES];
        
        NSUInteger buttonWidth = 160;
        _confirmButton.frame = CGRectMake(self.view.frame.size.width / 2 - buttonWidth / 2, 380, buttonWidth, 50);
        
        [_confirmButton setBackgroundColor:[UIColor systemBlueColor]];
        [_confirmButton.layer setBorderColor:[UIColor clearColor].CGColor];
        [_confirmButton setTitleColor:[UIColor whiteColor] forState:0];
        
        _confirmButton.titleLabel.font = [UIFont systemFontOfSize:20];
        [_confirmButton setTitle:@"查询" forState:0];
        
        [_confirmButton addTarget:self action:@selector(confirmButtonClick:) forControlEvents:UIControlEventTouchUpInside];
        
        _confirmButton.userInteractionEnabled = YES;
    }
    return _confirmButton;
}


- (void) confirmButtonClick:(id)sender {
    NSURLSessionConfiguration *defaultConfigObject = [NSURLSessionConfiguration defaultSessionConfiguration];
    NSURLSession *delegateFreeSession = [NSURLSession sessionWithConfiguration: defaultConfigObject
                                                                          delegate: self
                                                                     delegateQueue: [NSOperationQueue mainQueue]];
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat: @"http://172.16.207.150:8383/get_company_inf/?cpName=%@", self.inputField.text]];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];

    NSURLSessionDataTask * dataTask = [delegateFreeSession dataTaskWithRequest:request
        completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        if(error == nil) {
            NSString * text = [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
            NSData* jsonData = [text dataUsingEncoding:NSUTF8StringEncoding];
            NSDictionary* dic = [NSJSONSerialization JSONObjectWithData:jsonData options:NSJSONReadingAllowFragments error:&error];
            NSLog(@"%@", dic);
            if(dic[@"companyName"] != nil) {
            AppDelegate *myDelegate = (AppDelegate*)[[UIApplication sharedApplication]delegate];
            CompanyResultViewController* qc = [[CompanyResultViewController alloc] init];
            qc.title = @"查询结果";
            [qc.item1 setText: [NSString stringWithFormat:@"公司名称：%@", dic[@"companyName"]]];
            [qc.item2 setText: [NSString stringWithFormat:@"公司类型：%@", dic[@"companyType"]]];
            [qc.item3 setText: [NSString stringWithFormat:@"信用资产：%@", dic[@"creditAsset"]]];
            //NSLog(@"%ld", [dic[@"isTrusted"] integerValue]);
            if([dic[@"isTrusted"] integerValue] == 1) {
                [qc.item4 setText: @"是否受信：是"];
            }
            else {
                [qc.item4 setText: @"是否受信：否"];
            }
            
            [qc.item5 setText: [NSString stringWithFormat:@"真实资金：%@", dic[@"realMoney"]]];
            
            
                
            
            [myDelegate.nc pushViewController:qc animated:YES];
            }
            else {
                AppDelegate *myDelegate = (AppDelegate*)[[UIApplication sharedApplication]delegate];
                NoResultViewController* qc = [[NoResultViewController alloc] init];
                [myDelegate.nc pushViewController:qc animated:YES];
            }
            /*
            for(int i = 0; i < self->mainCollectionView.numberOfSections; i++) {
                QuestionCollectionViewCell *cell = (QuestionCollectionViewCell *)[self->mainCollectionView cellForItemAtIndexPath:[NSIndexPath indexPathForRow:0 inSection:i]];
                        
                [cell.QuestionButton setTitle:dic[@"data"][self->currentPage][@"choices"][i] forState:0];
            }
            self.QuestionLabel.text = dic[@"data"][self->currentPage][@"question"];
             */
        }
        }];
            
        [dataTask resume];
    

}




@end


